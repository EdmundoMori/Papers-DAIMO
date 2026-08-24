========================================================================
DAIMO-ISSUE-04 reused-class SHACL target scope harness
========================================================================
  OfferInDAIMOShape sh:targetClass = (none)
  OfferInDAIMOShape sh:targetObjectsOf = ['hasOfferPolicy']
  MachineLearningModelInDAIMOShape sh:targetClass = (none)
  MachineLearningModelInDAIMOShape sh:targetObjectsOf = ['deploysModel', 'offersModel']
  RunInDAIMOShape sh:targetClass = (none)
  RunInDAIMOShape sh:targetObjectsOf = ['authorizesRun', 'derivedFromRun']
  AgreementInDAIMOShape sh:targetClass = (none)
  AgreementInDAIMOShape sh:targetObjectsOf = ['derivedFromAgreement']

[external Offer/Model/Run incomplete] conforms=True focus=[]

[DAIMO Offer incomplete] conforms=False focus=['https://example.org/daimo-scope/offer-incomplete', 'https://example.org/daimo-scope/offering']

[DAIMO Model incomplete] conforms=False focus=['https://example.org/daimo-scope/model-incomplete']

[DAIMO Run incomplete] conforms=False focus=['https://example.org/daimo-scope/run-incomplete']

[DAIMO Offer/Model/Run complete (mixed with externals)] conforms=True focus=[]

PASS: 9-cell matrix — external incomplete ignored; in-scope incomplete rejected; in-scope complete conforms.
