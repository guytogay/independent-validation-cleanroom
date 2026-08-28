#!/usr/bin/env python3
from __future__ import annotations
from validate_retrieval_obligation import validate_document, build_sufficiency_resolution

def base_doc():
    d={"schema_version":"memory-retrieval-obligation-research-0.5","decisions":[{"decision_id":"d1","consequence":"MATERIAL","disposition":"READY","uncertainty_declared":False}],"trigger_events":[{"trigger_id":"t1","decision_id":"d1","basis":"GENERIC_REFLEX","resolver_ref":"resolver:logical"}],"retrieval_intents":[{"intent_id":"i1","decision_id":"d1","trigger_ids":["t1"],"resolver_ref":"resolver:logical","decision_context_snapshot_ref":"ctx:d1:v1","need_basis":"DURABLE_STATE_MAY_CHANGE_DECISION"}],"obligations":[{"obligation_id":"o1","decision_id":"d1","intent_id":"i1","resolver_ref":"resolver:logical","state":"CLOSED","closure":{"disposition":"RETRIEVAL_SUFFICIENCY_RESOLVED","basis_discovery_id":"sd1","basis_attempt_ids":["a1"],"sufficiency_resolution_ref":"suff:1"}}],"scope_discoveries":[{"discovery_id":"sd1","obligation_id":"o1","sequence":1,"resolver_ref":"resolver:logical","registry_snapshot_ref":"registry:v1","selected_scope_refs":["scope:A","scope:B"],"outcome":"SCOPES_SELECTED","coverage":"PARTIAL","subject_relevance":"DECISION_MATERIAL","receipt_ref":"disc:1"}],"attempts":[{"attempt_id":"a1","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:A","sequence":1,"resolver_ref":"resolver:logical","outcome":"HIT","coverage":"PARTIAL","subject_relevance":"DECISION_MATERIAL","returned_results":[{"record_ref":"M1","content_identity_ref":"sha256:V1"},{"record_ref":"M2","content_identity_ref":"sha256:V1"}],"receipt_ref":"ret:1"}],"sufficiency_resolutions":[]}
    d["sufficiency_resolutions"]=[build_sufficiency_resolution(d,"o1")]
    return d

def nohit_doc():
    d=base_doc(); d["obligations"][0]["closure"]={"disposition":"NO_HIT_BOUNDED","basis_discovery_id":"sd1","basis_attempt_ids":["a1","a2"]}; d["scope_discoveries"][0]["coverage"]="DECLARED_DISCOVERY_COMPLETE"; d["attempts"]=[{"attempt_id":"a1","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:A","sequence":1,"resolver_ref":"resolver:logical","outcome":"NO_HIT","coverage":"DECLARED_SCOPE_COMPLETE","subject_relevance":"DECISION_MATERIAL","returned_results":[],"receipt_ref":"ret:1"},{"attempt_id":"a2","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:B","sequence":2,"resolver_ref":"resolver:logical","outcome":"NO_HIT","coverage":"DECLARED_SCOPE_COMPLETE","subject_relevance":"DECISION_MATERIAL","returned_results":[],"receipt_ref":"ret:2"}]; d["sufficiency_resolutions"]=[]; return d

def expect(name,doc,valid):
    errors=validate_document(doc); got=not errors
    if got != valid: raise AssertionError(f"{name}: expected valid={valid}; errors={errors}")

def main():
    n=0
    d=base_doc(); expect("baseline",d,True); n+=1
    d=base_doc(); d["attempts"][0]["returned_results"][0]["content_identity_ref"]="sha256:V2"; expect("content_change_invalidates_old_resolution",d,False); n+=1
    d=base_doc(); d["attempts"][0]["returned_results"].reverse(); expect("returned_result_set_reorder_stable",d,True); n+=1
    d=base_doc(); d["scope_discoveries"][0]["selected_scope_refs"].reverse(); expect("scope_set_reorder_stable",d,True); n+=1
    d=base_doc(); d["scope_discoveries"].append({"discovery_id":"sd2","obligation_id":"o1","sequence":2,"resolver_ref":"resolver:logical","registry_snapshot_ref":"registry:v1","selected_scope_refs":[],"outcome":"FAILED","coverage":"UNKNOWN","subject_relevance":"NON_MATERIAL_OBSERVATION","receipt_ref":"disc:2"}); expect("later_nonmaterial_discovery_does_not_invalidate",d,True); n+=1
    d=base_doc(); d["scope_discoveries"].append({"discovery_id":"sd2","obligation_id":"o1","sequence":2,"resolver_ref":"resolver:logical","registry_snapshot_ref":"registry:v2","selected_scope_refs":[],"outcome":"FAILED","coverage":"UNKNOWN","subject_relevance":"DECISION_MATERIAL","receipt_ref":"disc:2"}); expect("later_material_discovery_invalidates_old_closure",d,False); n+=1
    d=base_doc(); d["attempts"].append({"attempt_id":"a2","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:B","sequence":2,"resolver_ref":"resolver:logical","outcome":"FAILED","coverage":"UNKNOWN","subject_relevance":"NON_MATERIAL_OBSERVATION","returned_results":[],"receipt_ref":"ret:2"}); expect("later_nonmaterial_attempt_does_not_invalidate",d,True); n+=1
    d=base_doc(); d["attempts"].append({"attempt_id":"a2","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:B","sequence":2,"resolver_ref":"resolver:logical","outcome":"NO_HIT","coverage":"PARTIAL","subject_relevance":"DECISION_MATERIAL","returned_results":[],"receipt_ref":"ret:2"}); expect("later_material_attempt_invalidates_old_resolution",d,False); n+=1
    d=base_doc(); d["scope_discoveries"][0]["subject_relevance"]="NON_MATERIAL_OBSERVATION"; expect("closure_basis_must_be_material",d,False); n+=1
    d=base_doc(); d["scope_discoveries"][0]["subject_relevance"]="NON_MATERIAL_OBSERVATION"; expect("nonmaterial_discovery_with_material_attempt_invalid",d,False); n+=1
    d={"schema_version":"memory-retrieval-obligation-research-0.5","decisions":[{"decision_id":"d1","consequence":"MATERIAL","disposition":"READY","uncertainty_declared":False}],"trigger_events":[],"retrieval_intents":[],"obligations":[],"scope_discoveries":[],"attempts":[],"sufficiency_resolutions":[]}; expect("runtime_cannot_detect_missing_trigger",d,True); n+=1
    d=base_doc(); d["obligations"][0]["closure"]={"disposition":"NO_HIT_BOUNDED","basis_discovery_id":"sd1","basis_attempt_ids":[]}; d["scope_discoveries"][0].update({"selected_scope_refs":[],"outcome":"NO_RELEVANT_SCOPE","coverage":"DECLARED_DISCOVERY_COMPLETE"}); d["attempts"]=[]; d["sufficiency_resolutions"]=[]; expect("false_complete_discovery_remains_external_residual",d,True); n+=1
    d=nohit_doc(); expect("nohit_bounded_valid",d,True); n+=1
    d=nohit_doc(); d["attempts"].append({"attempt_id":"a3","obligation_id":"o1","discovery_id":"sd1","scope_ref":"scope:A","sequence":3,"resolver_ref":"resolver:logical","outcome":"HIT","coverage":"PARTIAL","subject_relevance":"NON_MATERIAL_OBSERVATION","returned_results":[{"record_ref":"M3","content_identity_ref":"sha256:X"}],"receipt_ref":"ret:3"}); expect("nohit_cannot_ignore_any_represented_hit",d,False); n+=1
    d=base_doc(); d["retrieval_intents"][0]["decision_context_snapshot_ref"]="ctx:d1:v2"; expect("context_change_invalidates_old_resolution",d,False); n+=1
    d=base_doc(); d["attempts"][0]["returned_results"][0]["content_identity_ref"]="sha256:V2"; d["sufficiency_resolutions"]=[build_sufficiency_resolution(d,"o1")]; expect("fresh_resolution_after_content_change_valid",d,True); n+=1
    d=base_doc(); d["attempts"][0]["resolver_ref"]="resolver:physical-B"; expect("resolver_identity_mismatch_blocked",d,False); n+=1
    print(f"RETRIEVAL_OBLIGATION_05_SELFTEST_PASS {n}")

if __name__=="__main__": main()
