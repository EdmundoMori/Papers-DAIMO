========================================================================
DAIMO negative-test harness (cross-class invariants)
========================================================================
Ontology triples: 608
Shape triples   : 364
Negative triples: 163

SHACL conforms: False

  FOUND    INV-1  (looking for focus node containing 'INV1-artifact')
  FOUND    INV-2  (looking for focus node containing 'INV2-run')
  FOUND    INV-3  (looking for focus node containing 'INV3-deployment')
  FOUND    INV-4  (looking for focus node containing 'INV4-auth')
  FOUND    INV-5  (looking for focus node containing 'INV5-offering')
  FOUND    INV-6  (looking for focus node containing 'INV6-offering')
  FOUND    INV-7  (looking for focus node containing 'INV7-deployment')
  FOUND    INV-8  (looking for focus node containing 'INV8-deployment')

--- raw SHACL report (truncated) ---
Validation Report
Conforms: False
Results (14):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class dcat:DataService ; sh:maxCount Literal("1", datatype=xsd:integer) ; sh:message Literal("An I/O contract must identify exactly one dcat:DataService it applies to (daimo:forService).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path daimo:forService ]
	Focus Node: [ <https://w3id.org/pionera/daimo#authMethod> Literal("api-key") ; <https://w3id.org/pionera/daimo#inputFormat> Literal("application/json") ; <https://w3id.org/pionera/daimo#outputFormat> Literal("application/json") ; rdf:type <https://w3id.org/pionera/daimo#IOContract>, rdfs:Resource ]
	Result Path: daimo:forService
	Message: An I/O contract must identify exactly one dcat:DataService it applies to (daimo:forService).
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
	Value Node: [ odrl:permission [ odrl:action odrl:use ; rdf:type odrl:Permission, rdfs:Resource ] ; rd

PASS: all 8 invariants fired on their designated focus nodes.
