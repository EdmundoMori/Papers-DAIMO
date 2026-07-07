======================================================================
DAIMO validation runner
======================================================================

Ontology files : ['alignment.ttl', 'daimo-core.ttl']
Shape files    : ['daimo-shapes.ttl']
Example files  : ['flood-risk-scenario.ttl']

[1/3] Parsing Turtle files ...
  ontology triples : 593
  shape triples    : 342
  data triples     : 225

[2/3] Running SHACL validation ...
  conforms         : True

[3/3] Running CQ SPARQL queries ...
  found 23 CQ queries in queries.md
  materialised closure: 1988 triples
  PASS  CQ-R1     rows=3
  PASS  CQ-R2     rows=1
  PASS  CQ-R3     rows=1
  PASS  CQ-R4     rows=2
  PASS  CQ-R5     rows=2
  PASS  CQ-D1     rows=3
  PASS  CQ-D2     rows=2
  PASS  CQ-D3     rows=4
  PASS  CQ-D4     rows=1
  PASS  CQ-E1     rows=4
  PASS  CQ-E2     rows=1
  PASS  CQ-E3     rows=2
  PASS  CQ-E4     rows=1
  PASS  CQ-E5     rows=1
  PASS  CQ-V1     rows=1
  PASS  CQ-V2     rows=1
  PASS  CQ-V3     rows=2
  PASS  CQ-V4     rows=1
  PASS  CQ-V5     rows=4
  PASS  CQ-G1     rows=1
  PASS  CQ-G2     rows=2
  PASS  CQ-G3     rows=1
  PASS  CQ-G4     rows=1

======================================================================
Summary: 23/23 CQ queries return >=1 row; SHACL conforms=True
======================================================================
