#!/usr/bin/env python3
"""Research validator for Triggered Retrieval Obligation 0.5.

0.5 is a narrow reconciliation after independent review of 0.4:
- retrieval sufficiency binds effective returned-result identity, not bare record aliases;
- set-like subject components are normalized before fingerprinting;
- only later represented DECISION_MATERIAL discovery/attempt evidence changes the
  retrieval-sufficiency subject; NON_MATERIAL_OBSERVATION is retained but does not
  force semantic re-resolution;
- resolver_ref is a logical resolver / trust-equivalence identity, not necessarily
  a physical process identity.

PASS proves represented lifecycle consistency only. It does not authenticate Host
evaluators, prove materiality classifications, prove discovery/recall completeness,
or establish restore/current-world freshness.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parent
SCHEMA=ROOT/'retrieval-obligation.schema.json'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def index(items,key,errors,label):
    out={}
    for i,x in enumerate(items or []):
        k=x.get(key)
        if not k: errors.append(f'{label}[{i}] missing {key}')
        elif k in out: errors.append(f'duplicate {key} {k}')
        else: out[k]=x
    return out

def canon(x):
    if isinstance(x,dict): return {k:canon(v) for k,v in sorted(x.items()) if k!='notes'}
    if isinstance(x,list): return [canon(v) for v in x]
    return x

def normalize_discovery(d):
    x={k:v for k,v in d.items() if k!='notes'}
    x['selected_scope_refs']=sorted(x.get('selected_scope_refs',[]) or [])
    return canon(x)

def normalize_attempt(a):
    x={k:v for k,v in a.items() if k!='notes'}
    rr=x.get('returned_results',[]) or []
    x['returned_results']=sorted([canon(v) for v in rr],key=lambda r:(r.get('record_ref',''),r.get('content_identity_ref','')))
    return canon(x)

def fingerprint(x):
    return hashlib.sha256(json.dumps(canon(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def validate_document(doc):
    errors=[]
    schema=load(SCHEMA)
    errors += [f'schema: {e.message}' for e in Draft202012Validator(schema).iter_errors(doc)]
    decisions=index(doc.get('decisions'),'decision_id',errors,'decision')
    triggers=index(doc.get('trigger_events'),'trigger_id',errors,'trigger')
    intents=index(doc.get('retrieval_intents'),'intent_id',errors,'intent')
    obligations=index(doc.get('obligations'),'obligation_id',errors,'obligation')
    discoveries=index(doc.get('scope_discoveries'),'discovery_id',errors,'discovery')
    attempts=index(doc.get('attempts'),'attempt_id',errors,'attempt')
    resolutions=index(doc.get('sufficiency_resolutions'),'resolution_ref',errors,'sufficiency_resolution')

    trigger_owners={k:[] for k in triggers}; intent_owners={k:[] for k in intents}
    for tid,t in triggers.items():
        if t.get('decision_id') not in decisions: errors.append(f'{tid}: unknown decision')
    for iid,i in intents.items():
        did=i.get('decision_id'); resolver=i.get('resolver_ref')
        if did not in decisions: errors.append(f'{iid}: unknown decision')
        for tid in i.get('trigger_ids',[]) or []:
            t=triggers.get(tid)
            if not t: errors.append(f'{iid}: unknown trigger {tid}'); continue
            trigger_owners.setdefault(tid,[]).append(iid)
            if t.get('decision_id')!=did: errors.append(f'{iid}: trigger {tid} decision mismatch')
            if t.get('resolver_ref')!=resolver: errors.append(f'{iid}: trigger {tid} resolver mismatch')
    for tid,owners in trigger_owners.items():
        if len(owners)!=1: errors.append(f'{tid}: represented trigger must externalize exactly one retrieval intent; owners={owners}')

    for oid,o in obligations.items():
        iid=o.get('intent_id'); i=intents.get(iid)
        if not i: errors.append(f'{oid}: unknown intent {iid}')
        else:
            intent_owners.setdefault(iid,[]).append(oid)
            if o.get('decision_id')!=i.get('decision_id'): errors.append(f'{oid}: decision mismatch with intent')
            if o.get('resolver_ref')!=i.get('resolver_ref'): errors.append(f'{oid}: resolver mismatch with intent')
        if o.get('state')=='CLOSED' and not o.get('closure'): errors.append(f'{oid}: CLOSED requires closure')
        if o.get('state')!='CLOSED' and o.get('closure'): errors.append(f'{oid}: non-CLOSED must not carry closure')
    for iid,owners in intent_owners.items():
        if len(owners)!=1: errors.append(f'{iid}: retrieval intent must externalize exactly one obligation; owners={owners}')

    discoveries_by_obligation={k:[] for k in obligations}; discovery_sequences={k:{} for k in obligations}
    for did,d in discoveries.items():
        oid=d.get('obligation_id'); o=obligations.get(oid)
        if not o: errors.append(f'{did}: unknown obligation {oid}'); continue
        discoveries_by_obligation.setdefault(oid,[]).append(did)
        seq=d.get('sequence'); seqmap=discovery_sequences.setdefault(oid,{})
        if seq in seqmap: errors.append(f'{oid}: duplicate discovery sequence {seq} for {seqmap[seq]} and {did}')
        else: seqmap[seq]=did
        if d.get('resolver_ref')!=o.get('resolver_ref'): errors.append(f'{did}: resolver mismatch with obligation')
        scopes=d.get('selected_scope_refs',[]) or []; outcome=d.get('outcome')
        if outcome=='SCOPES_SELECTED' and not scopes: errors.append(f'{did}: SCOPES_SELECTED requires >=1 selected scope')
        if outcome in {'NO_RELEVANT_SCOPE','FAILED','UNKNOWN'} and scopes: errors.append(f'{did}: {outcome} must not claim selected scopes')

    attempts_by_obligation={k:[] for k in obligations}; attempts_by_discovery={k:[] for k in discoveries}; attempt_sequences={k:{} for k in discoveries}
    for aid,a in attempts.items():
        oid=a.get('obligation_id'); o=obligations.get(oid); d=discoveries.get(a.get('discovery_id'))
        if not o: errors.append(f'{aid}: unknown obligation {oid}'); continue
        attempts_by_obligation.setdefault(oid,[]).append(aid)
        if not d: errors.append(f'{aid}: unknown discovery {a.get("discovery_id")}'); continue
        attempts_by_discovery.setdefault(d.get('discovery_id'),[]).append(aid)
        seq=a.get('sequence'); seqmap=attempt_sequences.setdefault(d.get('discovery_id'),{})
        if seq in seqmap: errors.append(f'{d.get("discovery_id")}: duplicate attempt sequence {seq} for {seqmap[seq]} and {aid}')
        else: seqmap[seq]=aid
        if d.get('obligation_id')!=oid: errors.append(f'{aid}: discovery belongs to another obligation')
        if a.get('resolver_ref')!=o.get('resolver_ref') or a.get('resolver_ref')!=d.get('resolver_ref'): errors.append(f'{aid}: resolver mismatch')
        if d.get('outcome')!='SCOPES_SELECTED': errors.append(f'{aid}: attempts require SCOPES_SELECTED discovery')
        if a.get('scope_ref') not in (d.get('selected_scope_refs',[]) or []): errors.append(f'{aid}: scope not selected by discovery')
        if d.get('subject_relevance')=='NON_MATERIAL_OBSERVATION' and a.get('subject_relevance')!='NON_MATERIAL_OBSERVATION': errors.append(f'{aid}: non-material discovery cannot contain decision-material attempt')
        outcome=a.get('outcome'); returned=a.get('returned_results',[]) or []
        if outcome=='HIT' and not returned: errors.append(f'{aid}: HIT requires returned_results')
        if outcome=='NO_HIT' and returned: errors.append(f'{aid}: NO_HIT cannot return results')

    def material_discoveries(oid):
        return [discoveries[x] for x in discoveries_by_obligation.get(oid,[]) if x in discoveries and discoveries[x].get('subject_relevance')=='DECISION_MATERIAL']

    def current_material_discovery(oid):
        ds=material_discoveries(oid)
        return max(ds,key=lambda d:(d.get('sequence',0),d.get('discovery_id',''))) if ds else None

    def material_attempts(discovery_id):
        vals=[attempts[x] for x in attempts_by_discovery.get(discovery_id,[]) if x in attempts and attempts[x].get('subject_relevance')=='DECISION_MATERIAL']
        return sorted(vals,key=lambda a:(a.get('sequence',0),a.get('attempt_id','')))

    def suff_subject(oid,cd):
        o=obligations[oid]; i=intents.get(o.get('intent_id'),{}); d=decisions.get(o.get('decision_id'),{})
        return {'decision_id':o.get('decision_id'),'consequence':d.get('consequence'),'intent_id':o.get('intent_id'),'decision_context_snapshot_ref':i.get('decision_context_snapshot_ref'),'obligation_id':oid,'resolver_ref':o.get('resolver_ref'),'current_material_discovery':normalize_discovery(cd),'decision_material_attempts':[normalize_attempt(a) for a in material_attempts(cd.get('discovery_id'))]}

    satisfying={'RETRIEVAL_SUFFICIENCY_RESOLVED','NO_HIT_BOUNDED'}

    for oid,o in obligations.items():
        state=o.get('state')
        if state=='PENDING' and (discoveries_by_obligation.get(oid) or attempts_by_obligation.get(oid)): errors.append(f'{oid}: PENDING cannot already have activity')
        if state=='ATTEMPTED' and not discoveries_by_obligation.get(oid): errors.append(f'{oid}: ATTEMPTED requires discovery')
        if state!='CLOSED': continue
        c=o.get('closure') or {}; cd=discoveries.get(c.get('basis_discovery_id'))
        if not cd or cd.get('obligation_id')!=oid: errors.append(f'{oid}: closure basis_discovery_id must reference this obligation'); continue
        if cd.get('subject_relevance')!='DECISION_MATERIAL': errors.append(f'{oid}: closure basis discovery must be DECISION_MATERIAL')
        current=current_material_discovery(oid)
        if not current or cd.get('discovery_id')!=current.get('discovery_id'): errors.append(f'{oid}: closure must bind current represented decision-material discovery')

        basis_ids=c.get('basis_attempt_ids',[]) or []; basis=[]
        for aid in basis_ids:
            a=attempts.get(aid)
            if not a or a.get('obligation_id')!=oid: errors.append(f'{oid}: invalid closure basis attempt {aid}'); continue
            if a.get('discovery_id')!=cd.get('discovery_id'): errors.append(f'{oid}: closure attempt {aid} from another discovery')
            if a.get('subject_relevance')!='DECISION_MATERIAL': errors.append(f'{oid}: satisfying closure basis attempt {aid} must be DECISION_MATERIAL')
            basis.append(a)

        disp=c.get('disposition')
        if disp=='RETRIEVAL_SUFFICIENCY_RESOLVED':
            ref=c.get('sufficiency_resolution_ref'); packet=resolutions.get(ref)
            if not ref or not packet: errors.append(f'{oid}: RETRIEVAL_SUFFICIENCY_RESOLVED requires registered sufficiency resolution')
            elif current:
                expected=fingerprint(suff_subject(oid,current))
                if packet.get('subject_fingerprint')!=expected: errors.append(f'{oid}: sufficiency resolution subject fingerprint mismatch')
            if not any(a.get('outcome')=='HIT' and a.get('returned_results') for a in basis): errors.append(f'{oid}: RETRIEVAL_SUFFICIENCY_RESOLVED requires decision-material HIT basis attempt')
        elif c.get('sufficiency_resolution_ref'):
            errors.append(f'{oid}: sufficiency_resolution_ref only valid for RETRIEVAL_SUFFICIENCY_RESOLVED')

        if disp=='NO_HIT_BOUNDED':
            if cd.get('coverage')!='DECLARED_DISCOVERY_COMPLETE': errors.append(f'{oid}: NO_HIT_BOUNDED requires complete discovery')
            mats=material_attempts(cd.get('discovery_id'))
            if cd.get('outcome')=='NO_RELEVANT_SCOPE':
                if basis: errors.append(f'{oid}: NO_RELEVANT_SCOPE should not cite attempts')
                if mats: errors.append(f'{oid}: NO_RELEVANT_SCOPE cannot have decision-material attempts')
            elif cd.get('outcome')=='SCOPES_SELECTED':
                selected=set(cd.get('selected_scope_refs',[]) or [])
                all_disc_attempts=[attempts[x] for x in attempts_by_discovery.get(cd.get('discovery_id'),[]) if x in attempts]
                if any(a.get('outcome')=='HIT' for a in all_disc_attempts): errors.append(f'{oid}: NO_HIT_BOUNDED cannot ignore represented HIT')
                covered={a.get('scope_ref') for a in basis if a.get('outcome')=='NO_HIT' and a.get('coverage')=='DECLARED_SCOPE_COMPLETE'}
                if covered!=selected: errors.append(f'{oid}: NO_HIT_BOUNDED must cover every selected scope')
                mat_ids={a.get('attempt_id') for a in mats}
                if set(basis_ids)!=mat_ids: errors.append(f'{oid}: NO_HIT_BOUNDED must account for all decision-material basis-discovery attempts')
            else: errors.append(f'{oid}: invalid discovery outcome for NO_HIT_BOUNDED')

    obligations_by_decision={k:[] for k in decisions}
    for o in obligations.values(): obligations_by_decision.setdefault(o.get('decision_id'),[]).append(o)
    for did,d in decisions.items():
        obs=obligations_by_decision.get(did,[])
        unresolved=[o for o in obs if o.get('state')!='CLOSED']
        nonsatisfying=[o for o in obs if o.get('state')=='CLOSED' and (o.get('closure') or {}).get('disposition') not in satisfying]
        disp=d.get('disposition')
        if disp=='READY' and (unresolved or nonsatisfying): errors.append(f'{did}: READY requires bounded-no-hit or current-subject externally resolved sufficiency')
        if disp=='PROCEED_UNCERTAIN':
            if d.get('uncertainty_declared') is not True: errors.append(f'{did}: uncertainty must be declared')
            if d.get('consequence')=='MATERIAL': errors.append(f'{did}: MATERIAL cannot PROCEED_UNCERTAIN')
        if disp in {'NARROWED','ABSTAINED'} and d.get('uncertainty_declared') is not True: errors.append(f'{did}: {disp} requires uncertainty')
    return errors

def build_sufficiency_resolution(doc,obligation_id,resolution_ref='suff:1',receipt_ref='receipt:suff:1'):
    errors=[]
    decisions=index(doc.get('decisions'),'decision_id',errors,'decision'); intents=index(doc.get('retrieval_intents'),'intent_id',errors,'intent'); obligations=index(doc.get('obligations'),'obligation_id',errors,'obligation'); discoveries=index(doc.get('scope_discoveries'),'discovery_id',errors,'discovery'); attempts=index(doc.get('attempts'),'attempt_id',errors,'attempt')
    o=obligations[obligation_id]
    ds=[d for d in discoveries.values() if d.get('obligation_id')==obligation_id and d.get('subject_relevance')=='DECISION_MATERIAL']
    cd=max(ds,key=lambda d:(d.get('sequence',0),d.get('discovery_id','')))
    mats=sorted([a for a in attempts.values() if a.get('discovery_id')==cd.get('discovery_id') and a.get('subject_relevance')=='DECISION_MATERIAL'],key=lambda a:(a.get('sequence',0),a.get('attempt_id','')))
    i=intents[o['intent_id']]; dec=decisions[o['decision_id']]
    subject={'decision_id':o['decision_id'],'consequence':dec.get('consequence'),'intent_id':o['intent_id'],'decision_context_snapshot_ref':i.get('decision_context_snapshot_ref'),'obligation_id':obligation_id,'resolver_ref':o.get('resolver_ref'),'current_material_discovery':normalize_discovery(cd),'decision_material_attempts':[normalize_attempt(a) for a in mats]}
    return {'resolution_ref':resolution_ref,'subject_fingerprint':fingerprint(subject),'receipt_ref':receipt_ref}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path'); a=ap.parse_args(); doc=load(a.path); e=validate_document(doc)
    print(json.dumps({'valid':not e,'scope':'retrieval-obligation-0.5 represented lifecycle; Host truth/authentication/materiality remain external','errors':e},indent=2))
    raise SystemExit(0 if not e else 1)

if __name__=='__main__': main()
