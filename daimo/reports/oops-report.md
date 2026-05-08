# DAIMO OOPS! Pitfall Report

- Total pitfalls flagged: **2**
- Critical: **0**
- Important: **0**
- Minor: **2**

## Minor pitfalls (2)

### P13 — Inverse relationships not explicitly declared
- affected elements: 34
- description: This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.

### P04 — Creating unconnected ontology elements
- affected elements: 7
- description: Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.
- affected:
  - `http://www.w3.org/ns/prov#Bundle`
  - `http://www.w3.org/ns/odrl/2/Agreement`
  - `http://www.w3.org/ns/dcat#Catalog`
  - `http://www.w3.org/ns/dcat#Distribution`
  - `http://www.w3.org/ns/prov#Role`
  - `http://www.w3.org/ns/odrl/2/Permission`
  - `http://www.w3.org/ns/dcat#CatalogRecord`
