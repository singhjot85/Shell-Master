from jq_core.formatter import JQFormatter

def test_extract_base_jq_program():
    testcases = [
        "({.foo}//null)",
        "{.foo}",
        "(map(.bar)//null)",
        "(.[0])",
        "({foo:bar,baz:qux}//null)",
        "({foo:bar,baz:qux}//null)",
        "(({.foo}//null)|.bar)",
        "({.foo} | length)",
        "((({stuff}//null)|something) | other)"
    ]
    programs={
        "({.foo}//null)": "{.foo}",
        "{.foo}": "{.foo}",
    }
    starts = {
        "({.foo}//null)": "(",
        "{.foo}": "",
    }
    ends = {
        "({.foo}//null)": "//null)",
        "{.foo}": "",
    }
    for t in testcases:
        fomratter = JQFormatter()
        program, start, end =  fomratter.extract_base_jq_program(testcases)
        assert program == programs[t]
        assert start == starts[t]
        assert end == ends[t]

s = '''{ 
sbaLoanNumber: .sba_number,
sbaApplicationNumber: .sba_loan_app_number,
referenceNumber: (.application_number // null | tostring),
purposeType: (if $purposeType[.loan_purpose] then $purposeType[.loan_purpose] else "Other" end) ,
loanTermMonths: .term_in_months,
submittalDate: (if .submitted_date then .submitted_date | split("T")[0] else "" end),
impactWomanOwnedBusiness: .cra_female_owned_business,
impactVeteranOwnedBusiness: (if .details.boarding_details.veteran_owned_business == "yes" or .details.boarding_details.veteran_owned_business == "Yes" then true else false end),
impactMinorityOwnedBusiness: .cra_minority_owned_business,
loanType: (if .product.product_code == "7A_TL" then (if .loan_amount>500000 then "SBA 7(a)" else "SMALL SBA 7(a)" end) else $loanType[.product.product_code] end ),
loanStatus: "Funded",
loanAmount: (.approved_amount // null),
approvalDate: (.loan_decisioned_at // null),
closingDate: (.closing_date // null),
sbaProcessingMethodCode: "7AG",
impactLmi: .loan_relations[] | select(.is_primary_borrower == true) | .details.low_to_moderate_community,
sbssScore: (if .sbss_score then .sbss_score | tonumber else "" end),
sbssScoreDate:( try (.loan_interfaces[] | select(.interface_type == "fico" and .is_latest == true) | .details.fico_data.FI_LiquidCredit.timestamp | split(" ")[0] | strptime("%Y%m%d") | strftime("%Y-%m-%d") ) //null) ,
riskRatingGrade: .risk_rating,
riskRatingDate: (if .uw_completion_date then .uw_completion_date | split("T")[0] else "" end),
riskRatingReviewerContactId: .environment_values.lc_user_id ,
impactJobsCreatedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_created),
impactJobsRetainedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_saved),
achAccountName: .bank_details.bank_name,
achAccountNumber: .bank_details.account_number,
achRoutingNumber: .bank_details.routing_number,
achAccountType: .bank_details.account_type,
impactEmpowermentZoneEnterpriseCommunity: (.loan_relations[] | select(.is_primary_borrower == true) | .details.empowerment_zone),
impactHubZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.hub_zone),
impactPromiseZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.promise_zone),
impactRural: (.loan_relations[] | select(.is_primary_borrower == true) | .details.rural_zone),
impactOpportunityZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.opportunity_zone),
impactLowIncomeWorkforce: (.loan_relations[] | select(.is_primary_borrower == true) | .details.resides_in_low_income),
impactSbaVeteransAdvantage: (.loan_relations[] | select(.is_primary_borrower == true) | .details.eligibility_for_SBA_veterans),
collateralAnalysisNarrative: "Federal Flood Insurance if business location or collateral falls in a special flood hazard area, Worker's Compensation Insurance - upon hire of W-2 employees, Business Personal Property Insurance, full replacement costs, General Business Liability Insurance",
keyManInsuranceNarrative: "General Lending Guidelines do not require Key Man Life and Disability insurance for small business loans $350,000 or less.",
first2Years: (.loan_relations[] | select(.is_primary_borrower == true) | .details.new_businesses),
officeId: (if .details.boarding_details.branchCode then .details.boarding_details.branchCode | tonumber else null end),
interestRatePercent: .loan_approval.approved_rate,
sop: "50 10 7.1",
billingContactMethod: "Email",
billingEmail: (.loan_relations[] | select(.is_primary_borrower == true) | .email),
billingName: (.loan_relations[] | select(.is_primary_borrower == true) | .business_name),
primaryContactId: (if .primary_contact_id then .primary_contact_id | tonumber else null end),
referrals: [ 
{ 
contactId:  .environment_values.lc_user_id,
referralTypeId: 36,
fee1Description: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .fee_setup.fee.fee_name // null),
fee1Amount: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .approved_fee_amount // null),
fee1PaidBy: "Applicant",
fee3Description: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .fee_setup.fee.fee_name // null),
fee3Amount: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .approved_fee_amount // null),
fee3PaidBy: "Lender" 
} 
] ,
expenses:[.fees[] | select( .fee_setup.fee.fee_category == "origination") | { description:.fee_setup.fee.description,
amount:.approved_fee_amount,
date:(if .created then (.created | split("T")[0]) else "" end)}] ,
useOfProceeds: ( .uop_id_mapping as $UOPIdMapping | [ .use_of_proceed_details[] | 
{ 
useOfProceedTypeId: (if .purpose and $useOfProceedType[.purpose] and $UOPIdMapping[$useOfProceedType[.purpose]] then $UOPIdMapping[$useOfProceedType[.purpose]] else $UOPIdMapping["Others"] end),
Amount:(.amount|gsub(",|\\s";"")|tonumber) ,
Description: .name 
} 
]),
collaterals: ( .approved_amount as $loan_amount | .collateral_types_mapping as $CollateralTypesMapping | .environment_values.lien_holder_id as $lienHolderCompanyId | [ .loan_relations[] | .collaterals[] | 
{ 
collateralTypeId: (if .collateral_type and $collateralType[.collateral_type_verbose] and $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] then $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] else ( if .category and $collateralType[.category] and $CollateralTypesMapping[$collateralType[.category]] then $CollateralTypesMapping[$collateralType[.category]] else $CollateralTypesMapping["Other"] end) end),
value:(if .collateral_value then .collateral_value else $loan_amount end),
lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 elif .lien_position == "subordinate" then 2 else null end),
uccFiled:.is_ucc_filing_applicable,
liens:[ .lien_holders[] | 
{ 
lienHolderCompanyId: $lienHolderCompanyId ,
lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 else null end),
amount:.original_note_amount ,
Comment:(if .business_name and .business_name != "" then .business_name else .first_name + " " + .last_name end)
} 
] 
} 
] as $collaterals | $collaterals | map( . + {primary: (.value == ($collaterals | max_by(.value) | .value))} )),
mailingAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[] | select(.address_type == "mailing") | 
{ 
city: .city,
street1: .address_line_1,
street2: .address_line_2,
postalCode: .zip_code,
countryCode: .country,
stateCode: .state 
} 
),
projectAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[0] | 
{ 
city: .city,
street1: .address_line_1,
street2: .address_line_2,
postalCode: .zip_code,
countryCode: .country,
stateCode: .state 
} 
),
partners: [ 
{
contactId:  .environment_values.lc_user_id,
roleType: "LoanOfficer"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "LoanProcessor"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "ClosingOfficer"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "CreditAnalyst"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "ClosingAnalyst"
} 
],
entities : ( [ .flat_relations[] | select(
(
.party_type == "entity" 
and (.relation_type == "borrower" or .relation_type == "co_borrower" or .relation_type == "owner") 
and (.is_collateral_related | not)
) 
or (.party_type == "individual" 
and .entity_type == "sole_proprietor" 
and (.is_collateral_related | not) 
and .relation_type == "borrower")
) | 
( if (.entity_type == "sole_proprietor") then { 
primary: .is_primary_borrower,
association: "Operating Company",
guaranteeType: "Unsecured Limited",
company: 
{
name: ( if .dba_name and .dba_name !="" then .dba_name else .first_name + (if .middle_name and .middle_name != "" then " " + .middle_name else "" end) + " " + .last_name end ),
taxId: .tin,
taxIdType: .tin_type,
entityType: "Sole Proprietorship",
naicsCode: ( if .naics_code then .naics_code | tostring else null end ),
businessPhone: ((.work_phone|tostring) // null) 
} 
} 
else { 
companyId: (if .external_customer_id then .external_customer_id | tonumber else "" end),
borrower:true ,
association:(if .is_primary_borrower then "Operating Company" else "Affiliate" end) ,
annualRevenue:( .details.annual_business_revenue ),
guaranteeType:(if .is_primary_borrower == false and .ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end),
employeeCount: (if .is_primary_borrower then .number_of_employees else 0 end),
primary: .is_primary_borrower,
forms: [ (if .questionaire_responses[0] then 
{ 
name: "SBA1919_2023",
form: 
{ 
    question1: (if .questionaire_responses[0].responses.epc == "Yes" then true else false end),
    question2: (if .questionaire_responses[0].responses.defaulted == "Yes" then true else false end),
    question3: (if .questionaire_responses[0].responses.other_business == "Yes" then true else false end),
    question4: (if .questionaire_responses[0].responses.probation == "Yes" then true else false end),
    question5: (if .questionaire_responses[0].responses.exporting == "Yes" then true else false end),
    question7: (if .questionaire_responses[0].responses.gambling == "Yes" then true else false end),
    question8: (if .questionaire_responses[0].responses.sba_employee == "Yes" then true else false end),
    question9: (if .questionaire_responses[0].responses.sba_employee_2 == "Yes" then true else false end),
    question10: (if .questionaire_responses[0].responses.government == "Yes" then true else false end),
    question11: (if .questionaire_responses[0].responses.government_2 == "Yes" then true else false end),
    question12: (if .questionaire_responses[0].responses.sba_council == "Yes" then true else false end),
    question13: (if .questionaire_responses[0].responses.legal_action == "Yes" then true else false end) } } else empty end) ],
company: { 
name: .business_name,
stateOfFormation: .state_of_establishment,
currentOwnershipEstablishedDate: .business_established_date },
memberOf: [ { 
entityName: (if .memberof then .memberof else empty end),
ownershipPercentage: .ownership_percentage,
signer: (.is_signer),
controllingMember: (.is_ben_owner_by_control) } ] } end ) ] ),
contacts: [ .flat_relations[] as $loan_relations | select(
$loan_relations.party_type == "individual" 
and ($loan_relations.relation_type =="borrower" or $loan_relations.relation_type =="owner") 
and ($loan_relations.relation_type != "collateral_owner") 
and ($loan_relations.is_collateral_related | not) 
and ($loan_relations.is_system_created // false ) ) | { 
contactID: (if $loan_relations.external_customer_id != "" and $loan_relations.external_customer_id != null then $loan_relations.external_customer_id | tonumber else "" end),
guaranteeType:(if $loan_relations.ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end) ,
contact:{ 
firstName:$loan_relations.first_name,
lastName:$loan_relations.last_name,
creditScore:( try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | .details.fico.principals[] | select(.SSN == $loan_relations.tin) | .ficoScore | tonumber) //null),
creditScoreDate:(try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | (if .modified then .modified | split("T")[0] else "" end) ) // null) },
memberOf: ( if ($loan_relations.entity_type == "sole_proprietor") then [ {
entityName: ( if $loan_relations.dba_name and $loan_relations.dba_name !="" then $loan_relations.dba_name else $loan_relations.first_name + (if $loan_relations.middle_name and $loan_relations.middle_name != "" then " " + $loan_relations.middle_name else "" end) + " " + $loan_relations.last_name end),
ownershipPercentage: 100,
signer: ($loan_relations.is_signer),
controllingMember: ($loan_relations.is_ben_owner_by_control) 
} ] else [ { 
entityName: (if $loan_relations.memberof then $loan_relations.memberof else (if $loan_relations.entity_type == "sole_proprietor" then .borrower_name else empty end) end),
ownershipPercentage: $loan_relations.ownership_percentage,
signer: ($loan_relations.is_signer),
controllingMember: ($loan_relations.is_ben_owner_by_control) }]end)}]}'''
simple_program = '{"a":1,"b":"x,y","c":{"d":2,"e":[1,2,3]},"f":true}'
medium_program = """{
  apiSuccess: (if .responses|has("succeeded") then .responses|.succeeded else false end), 
  errors: .responses|.messages,
  responses: (
    if .responses|.succeeded and .result then 
        if (.responses.result | type == "array") then 
            [.responses.result[]]
        elif (.responses.result|type == "object") then 
            [.responses.result]
        else null end
  else null end)
}"""
complex_program="""{ 
    sbaLoanNumber: .sba_number,
    sbaApplicationNumber: .sba_loan_app_number,
    referenceNumber: (.application_number // null | tostring),
    purposeType: (if $purposeType[.loan_purpose] then $purposeType[.loan_purpose] else "Other" end) ,
    loanTermMonths: .term_in_months,
    submittalDate: (if .submitted_date then .submitted_date | split("T")[0] else "" end),
    impactWomanOwnedBusiness: .cra_female_owned_business,
    impactVeteranOwnedBusiness: (if .details.boarding_details.veteran_owned_business == "yes" or .details.boarding_details.veteran_owned_business == "Yes" then true else false end),
    impactMinorityOwnedBusiness: .cra_minority_owned_business,
    loanType: (if .product.product_code == "7A_TL" then (if .loan_amount>500000 then "SBA 7(a)" else "SMALL SBA 7(a)" end) else $loanType[.product.product_code] end ),
    loanStatus: "Funded",
    loanAmount: (.approved_amount // null),
    approvalDate: (.loan_decisioned_at // null),
    closingDate: (.closing_date // null),
    sbaProcessingMethodCode: "7AG",
    impactLmi: .loan_relations[] | select(.is_primary_borrower == true) | .details.low_to_moderate_community,
    sbssScore: (if .sbss_score then .sbss_score | tonumber else "" end),
    sbssScoreDate:( try (.loan_interfaces[] | select(.interface_type == "fico" and .is_latest == true) | .details.fico_data.FI_LiquidCredit.timestamp | split(" ")[0] | strptime("%Y%m%d") | strftime("%Y-%m-%d") ) //null) ,
    riskRatingGrade: .risk_rating,
    riskRatingDate: (if .uw_completion_date then .uw_completion_date | split("T")[0] else "" end),
    riskRatingReviewerContactId: .environment_values.lc_user_id ,
    impactJobsCreatedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_created),
    impactJobsRetainedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_saved),
    achAccountName: .bank_details.bank_name,
    achAccountNumber: .bank_details.account_number,
    achRoutingNumber: .bank_details.routing_number,
    achAccountType: .bank_details.account_type,
    impactEmpowermentZoneEnterpriseCommunity: (.loan_relations[] | select(.is_primary_borrower == true) | .details.empowerment_zone),
    impactHubZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.hub_zone),
    impactPromiseZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.promise_zone),
    impactRural: (.loan_relations[] | select(.is_primary_borrower == true) | .details.rural_zone),
    impactOpportunityZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.opportunity_zone),
    impactLowIncomeWorkforce: (.loan_relations[] | select(.is_primary_borrower == true) | .details.resides_in_low_income),
    impactSbaVeteransAdvantage: (.loan_relations[] | select(.is_primary_borrower == true) | .details.eligibility_for_SBA_veterans),
    collateralAnalysisNarrative: "Federal Flood Insurance if business location or collateral falls in a special flood hazard area, Worker's Compensation Insurance - upon hire of W-2 employees, Business Personal Property Insurance, full replacement costs, General Business Liability Insurance",
    keyManInsuranceNarrative: "General Lending Guidelines do not require Key Man Life and Disability insurance for small business loans $350,000 or less.",
    first2Years: (.loan_relations[] | select(.is_primary_borrower == true) | .details.new_businesses),
    officeId: (if .details.boarding_details.branchCode then .details.boarding_details.branchCode | tonumber else null end),
    interestRatePercent: .loan_approval.approved_rate,
    sop: "50 10 7.1",
    billingContactMethod: "Email",
    billingEmail: (.loan_relations[] | select(.is_primary_borrower == true) | .email),
    billingName: (.loan_relations[] | select(.is_primary_borrower == true) | .business_name),
    primaryContactId: (if .primary_contact_id then .primary_contact_id | tonumber else null end),
    referrals: [ 
        { 
            contactId:  .environment_values.lc_user_id,
            referralTypeId: 36,
            fee1Description: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .fee_setup.fee.fee_name // null),
            fee1Amount: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .approved_fee_amount // null),
            fee1PaidBy: "Applicant",
            fee3Description: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .fee_setup.fee.fee_name // null),
            fee3Amount: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .approved_fee_amount // null),
            fee3PaidBy: "Lender" 
        } 
    ] ,
    expenses:[.fees[] | select( .fee_setup.fee.fee_category == "origination") | { description:.fee_setup.fee.description,
    amount:.approved_fee_amount,
    date:(if .created then (.created | split("T")[0]) else "" end)}] ,
    useOfProceeds: ( .uop_id_mapping as $UOPIdMapping | [ .use_of_proceed_details[] | 
        { 
            useOfProceedTypeId: (if .purpose and $useOfProceedType[.purpose] and $UOPIdMapping[$useOfProceedType[.purpose]] then $UOPIdMapping[$useOfProceedType[.purpose]] else $UOPIdMapping["Others"] end),
            Amount:(.amount|gsub(",|\\s";"")|tonumber) ,
            Description: .name 
        } 
    ]),
    collaterals: ( .approved_amount as $loan_amount | .collateral_types_mapping as $CollateralTypesMapping | .environment_values.lien_holder_id as $lienHolderCompanyId | [ .loan_relations[] | .collaterals[] | 
        { 
            collateralTypeId: (if .collateral_type and $collateralType[.collateral_type_verbose] and $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] then $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] else ( if .category and $collateralType[.category] and $CollateralTypesMapping[$collateralType[.category]] then $CollateralTypesMapping[$collateralType[.category]] else $CollateralTypesMapping["Other"] end) end),
            value:(if .collateral_value then .collateral_value else $loan_amount end),
            lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 elif .lien_position == "subordinate" then 2 else null end),
            uccFiled:.is_ucc_filing_applicable,
            liens:[ .lien_holders[] | 
                { 
                    lienHolderCompanyId: $lienHolderCompanyId ,
                    lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 else null end),
                    amount:.original_note_amount ,
                    Comment:(if .business_name and .business_name != "" then .business_name else .first_name + " " + .last_name end)
                } 
            ] 
        } 
    ] as $collaterals | $collaterals | map( . + {primary: (.value == ($collaterals | max_by(.value) | .value))} )),
    mailingAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[] | select(.address_type == "mailing") | 
        { 
            city: .city,
            street1: .address_line_1,
            street2: .address_line_2,
            postalCode: .zip_code,
            countryCode: .country,
            stateCode: .state 
        } 
    ),
    projectAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[0] | 
        { 
            city: .city,
            street1: .address_line_1,
            street2: .address_line_2,
            postalCode: .zip_code,
            countryCode: .country,
            stateCode: .state 
        } 
    ),
    partners: [ 
        {
            contactId:  .environment_values.lc_user_id,
            roleType: "LoanOfficer"
        },
        {
            contactId:  .environment_values.lc_user_id,
            roleType: "LoanProcessor"
        },
        {
            contactId:  .environment_values.lc_user_id,
            roleType: "ClosingOfficer"
        },
        {
            contactId:  .environment_values.lc_user_id,
            roleType: "CreditAnalyst"
        },
        {
            contactId:  .environment_values.lc_user_id,
            roleType: "ClosingAnalyst"
        } 
    ],
    entities : ( [ .flat_relations[] | select(
        (
            .party_type == "entity" 
            and (.relation_type == "borrower" or .relation_type == "co_borrower" or .relation_type == "owner") 
            and (.is_collateral_related | not)
        ) 
        or (.party_type == "individual" 
        and .entity_type == "sole_proprietor" 
        and (.is_collateral_related | not) 
        and .relation_type == "borrower")
        ) | 
        ( if (.entity_type == "sole_proprietor") then { 
            primary: .is_primary_borrower,
            association: "Operating Company",
            guaranteeType: "Unsecured Limited",
            company: 
                {
                    name: ( if .dba_name and .dba_name !="" then .dba_name else .first_name + (if .middle_name and .middle_name != "" then " " + .middle_name else "" end) + " " + .last_name end ),
                    taxId: .tin,
                    taxIdType: .tin_type,
                    entityType: "Sole Proprietorship",
                    naicsCode: ( if .naics_code then .naics_code | tostring else null end ),
                    businessPhone: ((.work_phone|tostring) // null) 
                } 
        } 
        else { 
            companyId: (if .external_customer_id then .external_customer_id | tonumber else "" end),
            borrower:true ,
            association:(if .is_primary_borrower then "Operating Company" else "Affiliate" end) ,
            annualRevenue:( .details.annual_business_revenue ),
            guaranteeType:(if .is_primary_borrower == false and .ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end),
            employeeCount: (if .is_primary_borrower then .number_of_employees else 0 end),
            primary: .is_primary_borrower,
            forms: [ (if .questionaire_responses[0] then 
                { 
                    name: "SBA1919_2023",
                    form: 
                        { 
                            question1: (if .questionaire_responses[0].responses.epc == "Yes" then true else false end),
                            question2: (if .questionaire_responses[0].responses.defaulted == "Yes" then true else false end),
                            question3: (if .questionaire_responses[0].responses.other_business == "Yes" then true else false end),
                            question4: (if .questionaire_responses[0].responses.probation == "Yes" then true else false end),
                            question5: (if .questionaire_responses[0].responses.exporting == "Yes" then true else false end),
                            question7: (if .questionaire_responses[0].responses.gambling == "Yes" then true else false end),
                            question8: (if .questionaire_responses[0].responses.sba_employee == "Yes" then true else false end),
                            question9: (if .questionaire_responses[0].responses.sba_employee_2 == "Yes" then true else false end),
                            question10: (if .questionaire_responses[0].responses.government == "Yes" then true else false end),
                            question11: (if .questionaire_responses[0].responses.government_2 == "Yes" then true else false end),
                            question12: (if .questionaire_responses[0].responses.sba_council == "Yes" then true else false end),
                            question13: (if .questionaire_responses[0].responses.legal_action == "Yes" then true else false end) 
                        } 
                } else empty end) 
            ],
            company: 
                { 
                    name: .business_name,
                    stateOfFormation: .state_of_establishment,
                    currentOwnershipEstablishedDate: .business_established_date 
                },
            memberOf: [ 
                { 
                    entityName: (if .memberof then .memberof else empty end),
                    ownershipPercentage: .ownership_percentage,
                    signer: (.is_signer),
                    controllingMember: (.is_ben_owner_by_control) 
                } 
            ] 
        } end ) 
    ] ),
    contacts: [ .flat_relations[] as $loan_relations | select(
        $loan_relations.party_type == "individual" 
        and ($loan_relations.relation_type =="borrower" or $loan_relations.relation_type =="owner") 
        and ($loan_relations.relation_type != "collateral_owner") 
        and ($loan_relations.is_collateral_related | not) 
        and ($loan_relations.is_system_created // false ) ) | 
        { 
            contactID: (if $loan_relations.external_customer_id != "" and $loan_relations.external_customer_id != null then $loan_relations.external_customer_id | tonumber else "" end),
            guaranteeType:(if $loan_relations.ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end) ,
            contact:
                { 
                    firstName:$loan_relations.first_name,
                    lastName:$loan_relations.last_name,
                    creditScore:( try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | .details.fico.principals[] | select(.SSN == $loan_relations.tin) | .ficoScore | tonumber) //null),
                    creditScoreDate:(try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | (if .modified then .modified | split("T")[0] else "" end) ) // null) 
                },
            memberOf: ( if ($loan_relations.entity_type == "sole_proprietor") then [ 
                {
                    entityName: ( if $loan_relations.dba_name and $loan_relations.dba_name !="" then $loan_relations.dba_name else $loan_relations.first_name + (if $loan_relations.middle_name and $loan_relations.middle_name != "" then " " + $loan_relations.middle_name else "" end) + " " + $loan_relations.last_name end),
                    ownershipPercentage: 100,
                    signer: ($loan_relations.is_signer),
                    controllingMember: ($loan_relations.is_ben_owner_by_control) 
                } 
            ] else [ 
                { 
                    entityName: (if $loan_relations.memberof then $loan_relations.memberof else (if $loan_relations.entity_type == "sole_proprietor" then .borrower_name else empty end) end),
                    ownershipPercentage: $loan_relations.ownership_percentage,
                    signer: ($loan_relations.is_signer),
                    controllingMember: ($loan_relations.is_ben_owner_by_control) 
                } 
            ] end) 
        } 
    ] 
}"""
complex_program_1="""{ 
sbaLoanNumber: .sba_number,
sbaApplicationNumber: .sba_loan_app_number,
referenceNumber: (.application_number // null | tostring),
purposeType: (if $purposeType[.loan_purpose] then $purposeType[.loan_purpose] else "Other" end) ,
loanTermMonths: .term_in_months,
submittalDate: (if .submitted_date then .submitted_date | split("T")[0] else "" end),
impactWomanOwnedBusiness: .cra_female_owned_business,
impactVeteranOwnedBusiness: (if .details.boarding_details.veteran_owned_business == "yes" or .details.boarding_details.veteran_owned_business == "Yes" then true else false end),
impactMinorityOwnedBusiness: .cra_minority_owned_business,
loanType: (if .product.product_code == "7A_TL" then (if .loan_amount>500000 then "SBA 7(a)" else "SMALL SBA 7(a)" end) else $loanType[.product.product_code] end ),
loanStatus: "Funded",
loanAmount: (.approved_amount // null),
approvalDate: (.loan_decisioned_at // null),
closingDate: (.closing_date // null),
sbaProcessingMethodCode: "7AG",
impactLmi: .loan_relations[] | select(.is_primary_borrower == true) | .details.low_to_moderate_community,
sbssScore: (if .sbss_score then .sbss_score | tonumber else "" end),
sbssScoreDate:( try (.loan_interfaces[] | select(.interface_type == "fico" and .is_latest == true) | .details.fico_data.FI_LiquidCredit.timestamp | split(" ")[0] | strptime("%Y%m%d") | strftime("%Y-%m-%d") ) //null) ,
riskRatingGrade: .risk_rating,
riskRatingDate: (if .uw_completion_date then .uw_completion_date | split("T")[0] else "" end),
riskRatingReviewerContactId: .environment_values.lc_user_id ,
impactJobsCreatedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_created),
impactJobsRetainedByLoan: (.loan_relations[] | select(.is_primary_borrower == true) | .questionaire_responses[0].responses.jobs_saved),
achAccountName: .bank_details.bank_name,
achAccountNumber: .bank_details.account_number,
achRoutingNumber: .bank_details.routing_number,
achAccountType: .bank_details.account_type,
impactEmpowermentZoneEnterpriseCommunity: (.loan_relations[] | select(.is_primary_borrower == true) | .details.empowerment_zone),
impactHubZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.hub_zone),
impactPromiseZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.promise_zone),
impactRural: (.loan_relations[] | select(.is_primary_borrower == true) | .details.rural_zone),
impactOpportunityZone: (.loan_relations[] | select(.is_primary_borrower == true) | .details.opportunity_zone),
impactLowIncomeWorkforce: (.loan_relations[] | select(.is_primary_borrower == true) | .details.resides_in_low_income),
impactSbaVeteransAdvantage: (.loan_relations[] | select(.is_primary_borrower == true) | .details.eligibility_for_SBA_veterans),
collateralAnalysisNarrative: "Federal Flood Insurance if business location or collateral falls in a special flood hazard area, Worker's Compensation Insurance - upon hire of W-2 employees, Business Personal Property Insurance, full replacement costs, General Business Liability Insurance",
keyManInsuranceNarrative: "General Lending Guidelines do not require Key Man Life and Disability insurance for small business loans $350,000 or less.",
first2Years: (.loan_relations[] | select(.is_primary_borrower == true) | .details.new_businesses),
officeId: (if .details.boarding_details.branchCode then .details.boarding_details.branchCode | tonumber else null end),
interestRatePercent: .loan_approval.approved_rate,
sop: "50 10 7.1",
billingContactMethod: "Email",
billingEmail: (.loan_relations[] | select(.is_primary_borrower == true) | .email),
billingName: (.loan_relations[] | select(.is_primary_borrower == true) | .business_name),
primaryContactId: (if .primary_contact_id then .primary_contact_id | tonumber else null end),
referrals: [ 
{ 
contactId:  .environment_values.lc_user_id,
referralTypeId: 36,
fee1Description: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .fee_setup.fee.fee_name // null),
fee1Amount: (.fees[] | select(.fee_setup.fee.fee_code == "express_loan_packaging_fee") | .approved_fee_amount // null),
fee1PaidBy: "Applicant",
fee3Description: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .fee_setup.fee.fee_name // null),
fee3Amount: (.fees[] | select(.fee_setup.fee.fee_code == "broker_or_referral_fee") | .approved_fee_amount // null),
fee3PaidBy: "Lender" 
} 
] ,
expenses:[.fees[] | select( .fee_setup.fee.fee_category == "origination") | { description:.fee_setup.fee.description,
amount:.approved_fee_amount,
date:(if .created then (.created | split("T")[0]) else "" end)}] ,
useOfProceeds: ( .uop_id_mapping as $UOPIdMapping | [ .use_of_proceed_details[] | 
{ 
useOfProceedTypeId: (if .purpose and $useOfProceedType[.purpose] and $UOPIdMapping[$useOfProceedType[.purpose]] then $UOPIdMapping[$useOfProceedType[.purpose]] else $UOPIdMapping["Others"] end),
Amount:(.amount|gsub(",|\\s";"")|tonumber) ,
Description: .name 
} 
]),
collaterals: ( .approved_amount as $loan_amount | .collateral_types_mapping as $CollateralTypesMapping | .environment_values.lien_holder_id as $lienHolderCompanyId | [ .loan_relations[] | .collaterals[] | 
{ 
collateralTypeId: (if .collateral_type and $collateralType[.collateral_type_verbose] and $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] then $CollateralTypesMapping[$collateralType[.collateral_type_verbose]] else ( if .category and $collateralType[.category] and $CollateralTypesMapping[$collateralType[.category]] then $CollateralTypesMapping[$collateralType[.category]] else $CollateralTypesMapping["Other"] end) end),
value:(if .collateral_value then .collateral_value else $loan_amount end),
lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 elif .lien_position == "subordinate" then 2 else null end),
uccFiled:.is_ucc_filing_applicable,
liens:[ .lien_holders[] | 
{ 
lienHolderCompanyId: $lienHolderCompanyId ,
lienPosition:(if .lien_position == "first" then 1 elif .lien_position == "second" then 2 elif .lien_position == "third" then 3 elif .lien_position == "fourth" then 4 elif .lien_position == "fifth" then 5 else null end),
amount:.original_note_amount ,
Comment:(if .business_name and .business_name != "" then .business_name else .first_name + " " + .last_name end)
} 
] 
} 
] as $collaterals | $collaterals | map( . + {primary: (.value == ($collaterals | max_by(.value) | .value))} )),
mailingAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[] | select(.address_type == "mailing") | 
{ 
city: .city,
street1: .address_line_1,
street2: .address_line_2,
postalCode: .zip_code,
countryCode: .country,
stateCode: .state 
} 
),
projectAddress: ( .loan_relations[] | select(.is_primary_borrower == true) | .relation_addresses[0] | 
{ 
city: .city,
street1: .address_line_1,
street2: .address_line_2,
postalCode: .zip_code,
countryCode: .country,
stateCode: .state 
} 
),
partners: [ 
{
contactId:  .environment_values.lc_user_id,
roleType: "LoanOfficer"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "LoanProcessor"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "ClosingOfficer"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "CreditAnalyst"
},
{
contactId:  .environment_values.lc_user_id,
roleType: "ClosingAnalyst"
} 
],
entities : ( [ .flat_relations[] | select(
(
.party_type == "entity" 
and (.relation_type == "borrower" or .relation_type == "co_borrower" or .relation_type == "owner") 
and (.is_collateral_related | not)
) 
or (.party_type == "individual" 
and .entity_type == "sole_proprietor" 
and (.is_collateral_related | not) 
and .relation_type == "borrower")
) | 
( if (.entity_type == "sole_proprietor") then { 
primary: .is_primary_borrower,
association: "Operating Company",
guaranteeType: "Unsecured Limited",
company: 
{
name: ( if .dba_name and .dba_name !="" then .dba_name else .first_name + (if .middle_name and .middle_name != "" then " " + .middle_name else "" end) + " " + .last_name end ),
taxId: .tin,
taxIdType: .tin_type,
entityType: "Sole Proprietorship",
naicsCode: ( if .naics_code then .naics_code | tostring else null end ),
businessPhone: ((.work_phone|tostring) // null) 
} 
} 
else { 
companyId: (if .external_customer_id then .external_customer_id | tonumber else "" end),
borrower:true ,
association:(if .is_primary_borrower then "Operating Company" else "Affiliate" end) ,
annualRevenue:( .details.annual_business_revenue ),
guaranteeType:(if .is_primary_borrower == false and .ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end),
employeeCount: (if .is_primary_borrower then .number_of_employees else 0 end),
primary: .is_primary_borrower,
forms: [ (if .questionaire_responses[0] then 
{ 
name: "SBA1919_2023",
form: 
{ 
    question1: (if .questionaire_responses[0].responses.epc == "Yes" then true else false end),
    question2: (if .questionaire_responses[0].responses.defaulted == "Yes" then true else false end),
    question3: (if .questionaire_responses[0].responses.other_business == "Yes" then true else false end),
    question4: (if .questionaire_responses[0].responses.probation == "Yes" then true else false end),
    question5: (if .questionaire_responses[0].responses.exporting == "Yes" then true else false end),
    question7: (if .questionaire_responses[0].responses.gambling == "Yes" then true else false end),
    question8: (if .questionaire_responses[0].responses.sba_employee == "Yes" then true else false end),
    question9: (if .questionaire_responses[0].responses.sba_employee_2 == "Yes" then true else false end),
    question10: (if .questionaire_responses[0].responses.government == "Yes" then true else false end),
    question11: (if .questionaire_responses[0].responses.government_2 == "Yes" then true else false end),
    question12: (if .questionaire_responses[0].responses.sba_council == "Yes" then true else false end),
    question13: (if .questionaire_responses[0].responses.legal_action == "Yes" then true else false end) } } else empty end) ],
company: { 
name: .business_name,
stateOfFormation: .state_of_establishment,
currentOwnershipEstablishedDate: .business_established_date },
memberOf: [ { 
entityName: (if .memberof then .memberof else empty end),
ownershipPercentage: .ownership_percentage,
signer: (.is_signer),
controllingMember: (.is_ben_owner_by_control) } ] } end ) ] ),
contacts: [ .flat_relations[] as $loan_relations | select(
$loan_relations.party_type == "individual" 
and ($loan_relations.relation_type =="borrower" or $loan_relations.relation_type =="owner") 
and ($loan_relations.relation_type != "collateral_owner") 
and ($loan_relations.is_collateral_related | not) 
and ($loan_relations.is_system_created // false ) ) | { 
contactID: (if $loan_relations.external_customer_id != "" and $loan_relations.external_customer_id != null then $loan_relations.external_customer_id | tonumber else "" end),
guaranteeType:(if $loan_relations.ownership_percentage>20 then "Unsecured Full" else "Unsecured Limited" end) ,
contact:{ 
firstName:$loan_relations.first_name,
lastName:$loan_relations.last_name,
creditScore:( try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | .details.fico.principals[] | select(.SSN == $loan_relations.tin) | .ficoScore | tonumber) //null),
creditScoreDate:(try (.loan_aggregator[] | select(.aggregator_type == "fico" and .is_latest == true) | (if .modified then .modified | split("T")[0] else "" end) ) // null) },
memberOf: ( if ($loan_relations.entity_type == "sole_proprietor") then [ {
entityName: ( if $loan_relations.dba_name and $loan_relations.dba_name !="" then $loan_relations.dba_name else $loan_relations.first_name + (if $loan_relations.middle_name and $loan_relations.middle_name != "" then " " + $loan_relations.middle_name else "" end) + " " + $loan_relations.last_name end),
ownershipPercentage: 100,
signer: ($loan_relations.is_signer),
controllingMember: ($loan_relations.is_ben_owner_by_control) 
} ] else [ { 
entityName: (if $loan_relations.memberof then $loan_relations.memberof else (if $loan_relations.entity_type == "sole_proprietor" then .borrower_name else empty end) end),
ownershipPercentage: $loan_relations.ownership_percentage,
signer: ($loan_relations.is_signer),
controllingMember: ($loan_relations.is_ben_owner_by_control) }]end)}]}
"""

# Parser
from jq_core.parser import BaseParser
parsed = BaseParser().parse_sts(s)

# Formatter
from jq_core.formatter import tokenize_jq
result = tokenize_jq(parsed)
print(result)
