========================================================================
DAIMO negative-test harness (cross-class invariants)
========================================================================
Ontology triples: 592
Shape triples   : 342
Negative triples: 118

SHACL conforms: False

  FOUND    INV-1  (looking for focus node containing 'INV1-artifact')
  FOUND    INV-2  (looking for focus node containing 'INV2-run')
  FOUND    INV-3  (looking for focus node containing 'INV3-deployment')
  FOUND    INV-4  (looking for focus node containing 'INV4-auth')
  FOUND    INV-5  (looking for focus node containing 'INV5-offering')
  FOUND    INV-6  (looking for focus node containing 'INV6-offering')

--- raw SHACL report (truncated) ---
Validation Report
Conforms: False
Results (10):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:message Literal("An odrl:Offer must declare its assigner (the party issuing the offer).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path odrl:assigner ]
	Focus Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Result Path: odrl:assigner
	Message: An odrl:Offer must declare its assigner (the party issuing the offer).
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:message Literal("An odrl:Offer must declare its assigner (the party issuing the offer).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path odrl:assigner ]
	Focus Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Result Path: odrl:assigner
	Message: An odrl:Offer must declare its assigner (the party issuing the offer).
Constraint Violation in OrConstraintComponent (http://www.w3.org/ns/shacl#OrConstraintComponent):
	Severity: sh:Violation
	Source Shape: daimo:OfferInDAIMOShape
	Focus Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Value Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Message: An odrl:Offer must declare odrl:target at either Policy level or on each Permission.
Constraint Violation in OrConstraintComponent (http://www.w3.org/ns/shacl#OrConstraintComponent):
	Severity: sh:Violation
	Source Shape: daimo:OfferInDAIMOShape
	Focus Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Value Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rdf:type odrl:Offer, odrl:Policy, rdfs:Resource ]
	Message: An odrl:Offer must declare odrl:target at either Policy level or on each Permission.
Constraint Violation in SPARQLConstraintComponent (http://www.w3.org/ns/shacl#SPARQLConstraintComponent):
	Severity: sh:Violation
	Source Shape: daimo:AuthorizationTe

PASS: all 6 invariants fired on their designated focus nodes.
