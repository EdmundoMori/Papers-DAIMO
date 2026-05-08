# Dataspace Context for DAIMO: Eclipse EDC and INESData

Date: 2026-04-20

## 1. Why these two matter

For DAIMO, `Eclipse EDC` and `INESData` should not be treated as the same kind of source.

- `Eclipse EDC` gives the core dataspace runtime and protocol semantics.
- `INESData` shows how a concrete dataspace platform operationalizes those semantics in a real multi-participant environment, with portals, registration, shared vocabularies, and domain services.

This distinction matters because DAIMO should not confuse:
- protocol/runtime concepts,
- platform governance concepts,
- AI/ML asset concepts,
- domain application concepts.

## 2. What EDC contributes

Official EDC documentation makes the control plane responsibilities explicit:
- assembling catalogs,
- creating contract agreements,
- managing data transfers,
- monitoring policy compliance.

EDC concepts most relevant for ontology design:
- `Participant ID`
- `Asset`
- `DataAddress`
- `PolicyDefinition`
- `ContractDefinition`
- `Catalog`
- `Dataset`
- `Distribution`
- `DataService`
- `ContractNegotiation`
- `ContractAgreement`
- `TransferProcess`
- `Endpoint Data Reference`
- `Data Plane`

Important modeling points from the docs:
- An `Asset` is a descriptor, not the underlying bytes.
- `DataAddress` points to the physical source or destination.
- Policies are expressed in `ODRL`.
- Contract definitions bind assets to policies.
- Catalogs are dynamically generated for a participant.
- Contract negotiations are asynchronous.
- Transfer processes are separate from contract negotiations.
- Transfers can be finite or non-finite.
- Data can be file-based, streaming, or API-based.
- Ongoing transfers can be monitored against policy.

EDC also makes heavy use of:
- `DCAT` for catalogs, datasets, distributions, and services
- `ODRL` for offers, agreements, duties, permissions, and prohibitions
- `JSON-LD` expansion for extensible asset metadata

This means EDC is not just “infrastructure.”
It already gives a semantic process model for:
- publication,
- access control,
- agreement,
- exchange,
- transfer state,
- participant-bound interactions.

## 3. Newer EDC direction that matters

A 2025 EDC decision record introduces `ParticipantContext` for multi-participant workloads in one runtime.
It explicitly says the following entities will carry `participantContextId`:
- `Asset`
- `PolicyDefinition`
- `ContractDefinition`
- `ContractNegotiation`
- `ContractAgreement`
- `TransferProcess`
- `DataPlaneInstance`
- `EndpointDataReferenceEntry`

This is highly relevant for DAIMO because it shows the EDC model is moving from:
- one runtime = one participant

to:
- one runtime may host multiple participant contexts

For ontology design, this suggests we should distinguish:
- technical runtime,
- participant,
- participant context,
- dataspace profile context.

## 4. What INESData contributes

INESData explicitly describes itself as a Spanish incubator of data spaces and AI services using federated cloud infrastructures.
Its public repos show it is not only a connector fork, but a fuller platform around EDC.

### 4.1 Connector layer

The `inesdata-connector` repo states it is:
- a dataspaces connector for the INESData project,
- based on the EDC dataspaces framework.

So the connector layer is clearly derived from EDC.

### 4.2 Management and user-facing layer

The `inesdata-connector-interface` repo is a frontend for the EDC Management API.
Its configuration shows explicit support for:
- management API
- federated catalog API
- shared services
- assets
- contract agreements
- policy definitions
- contract definitions
- contract negotiations
- transfer processes
- shared vocabularies
- federated catalog pagination/count
- OAuth2 via Keycloak

The presence of:
- `/management/federatedcatalog`
- `/shared/connector-vocabularies`
- `/vocabularies`
- `/v3/inesdatatransferprocesses`

shows INESData adds platform-specific services beyond stock EDC concepts.

### 4.3 Registration and federation layer

The `inesdata-registration-service` repo states it manages and federates the participant catalog through a centralized `RegistrationService`.
It provides:
- public endpoints for connectors to retrieve participant information
- administrative endpoints for participant management
- connector-token access
- admin-user-token access

This is a very important semantic addition.
EDC itself models participant identity operationally, but INESData adds:
- participant registration,
- participant catalog federation,
- role-based participant administration.

### 4.4 Local environment and deployment pattern

The `inesdata-espacio-linguistico` local environment repo shows an actual multi-component dataspace deployment with:
- multiple connectors
- Keycloak
- Vault
- PostgreSQL
- MinIO
- Strapi CMS
- public portal
- management interfaces

Its connector configuration files show:
- `edc.participant.id` for each connector
- separate management, protocol, control, public, shared, and federated catalog endpoints
- OAuth2 / Keycloak integration
- a configured participant list for catalog crawling
- a registration service host
- periodic cache/crawler jobs
- a vocabulary synchronization task

This is strong evidence that INESData’s dataspace model includes:
- participant federation,
- federated catalog harvesting,
- shared vocabularies,
- identity and role management,
- platform-level synchronization jobs.

### 4.5 Domain layer

INESData repos also show domain applications on top of the dataspace:
- language-space integration and ELG connector pieces
- mobility AI services such as bus arrival predictions
- INESData Map for mapping rules and knowledge graph generation
- public portal and CMS-backed pages

This means INESData is not only about generic sharing.
It is a platform for domain-specific services and AI-enabled applications over the dataspace.

## 5. Clean separation for DAIMO

Based on these sources, the clean ontology layering for DAIMO should be:

### Layer A. Dataspace runtime/process layer

Owned mostly by EDC concepts:
- participant
- participant context
- asset descriptor
- data address
- access service
- catalog offer
- policy definition
- contract definition
- contract negotiation
- contract agreement
- transfer process
- endpoint data reference
- data plane instance

### Layer B. Dataspace platform/governance layer

Strongly motivated by INESData:
- participant registration
- participant directory/catalog
- participant roles
- connector administration roles
- shared vocabulary management
- federated catalog aggregation
- portal/publication context
- platform-level synchronization and cache tasks

### Layer C. AI/ML asset layer

This is where MLDCAT-AP should dominate:
- machine learning model
- dataset
- benchmark
- evaluation
- run
- flow
- modality
- risk
- model file
- service serving a model

### Layer D. Domain application layer

INESData examples show this layer may include:
- language resources and connectors
- mobility prediction services
- knowledge graph mapping services
- domain-specific public datasets and APIs

## 6. What DAIMO should probably add

From EDC + INESData + MLDCAT-AP together, the likely DAIMO gap is not “model metadata.”
It is the bridge between:
- an AI model as a governed asset,
- a dataspace participant offering it,
- the policies and agreements controlling it,
- the service or transfer mechanism exposing it,
- the provenance/evidence produced by its use in the dataspace.

Likely DAIMO-native additions:
- `AIAssetOffering` or equivalent bridge between model asset and dataspace offer
- `ParticipantRole` and possibly `ParticipantContext`
- `GovernedModelService` to distinguish service/API from file/package
- `ExchangeAgreement` aligned with ODRL agreement but specialized for AI asset usage in a dataspace
- `ExecutionAuthorization`
- `DerivedArtifact` or `ExecutionResultArtifact`
- `CrossParticipantProvenance`
- `SharedVocabulary` / `ConnectorVocabulary` if vocabularies are operationally important
- `FederatedCatalogEntry` if INESData-style aggregation is part of the scenario

## 7. Bottom line

EDC gives us the semantics of:
- how assets are offered,
- how access is negotiated,
- how policy is enforced,
- how transfer happens.

INESData gives us the semantics of:
- how participants are organized in a real platform,
- how catalogs are federated,
- how vocabularies and portals are managed,
- how domain services and AI applications sit on top.

So for DAIMO:
- `EDC` should shape the dataspace interaction model,
- `MLDCAT-AP` should shape the AI/ML metadata model,
- `INESData` should shape the platform/federation/governance requirements,
- and DAIMO should be the integration ontology/profile that connects those layers cleanly.

## Sources

- EDC Connector README: https://github.com/eclipse-edc/Connector/blob/main/README.md
- EDC control plane docs: https://github.com/eclipse-edc/eclipse-edc.github.io/blob/main/content/en/documentation/for-adopters/control-plane/_index.md
- EDC control-plane entities docs: https://github.com/eclipse-edc/eclipse-edc.github.io/blob/main/content/en/documentation/for-contributors/control-plane/entities/_index.md
- EDC participant context decision record: https://github.com/eclipse-edc/Connector/blob/main/docs/developer/decision-records/2025-08-26-participant-context/README.md
- INESData connector README: https://github.com/INESData/inesdata-connector/blob/develop/README.md
- INESData connector interface README: https://github.com/INESData/inesdata-connector-interface/blob/develop/README.md
- INESData connector interface config: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/assets/config/app.config.json
- INESData catalog browser service: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/app/shared/services/catalog-browser.service.ts
- INESData vocabulary service: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/app/shared/services/vocabulary.service.ts
- INESData registration service README: https://github.com/INESData/inesdata-registration-service/blob/develop/README.md
- INESData local environment README: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/README.md
- INESData connector configuration `c1`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-c1-configuration.properties
- INESData connector configuration `c2`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-c2-configuration.properties
- INESData connector configuration `elg`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-elg-configuration.properties
- INESData Map README: https://github.com/INESData/inesdata-map/blob/main/README.md
- INESData mobility AI service README: https://github.com/INESData/inesdata-mov-ai-service/blob/develop/README.md
