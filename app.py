from flask import Flask, render_template, request, redirect

import pandas as pd
import numpy as np
import altair as alt
from scipy import stats
import dill
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
    
    
app = Flask(__name__)

# Defining variables in dropdown menus:
slist=[
 'OperatingIncomeLoss',
 'NetIncomeLoss',
 'Revenues',
 'RevenueFromRelatedParties',
 'TaxableIncome',
 'TaxableIncomeDomestic',
 'TaxableIncomeForeign',
 'DiscontinuedOperationIncomeLossFromDiscontinuedOperationBeforeIncomeTax',
 'IncomeTaxExpenseBenefit',
 'DeferredIncomeTaxExpenseBenefit',
 'DeferredFederalIncomeTaxExpenseBenefit',
 'DeferredForeignIncomeTaxExpenseBenefit',
 'DeferredStateAndLocalIncomeTaxExpenseBenefit',
 'CurrentIncomeTaxExpenseBenefit',
 'CurrentFederalTaxExpenseBenefit',
 'CurrentForeignTaxExpenseBenefit',
 'CurrentStateAndLocalTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefitContinuingOperations',
 'StateAndLocalIncomeTaxExpenseBenefitContinuingOperations',
 'ForeignIncomeTaxExpenseBenefitContinuingOperations',
 'DomesticIncomeTaxExpenseBenefit',
 'StateAndLocalIncomeTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefit',
 'ForeignIncomeTaxExpenseBenefit',
 'DeferredTaxLiabilities',
 'AccruedIncomeTaxes',
 'AccruedIncomeTaxesCurrent',
 'AccruedIncomeTaxesNoncurrent',
 'UnrecognizedTaxBenefits',
 'UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate',
 'IncomeTaxesPaidNet',
 'IncreaseDecreaseInAccruedIncomeTaxesPayable',
 'EffectiveIncomeTaxRateReconciliationShareBasedCompensationExcessTaxBenefit',
 'IncomeTaxReconciliationShareBasedCompensationExcessTaxBenefit',
 'EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate',
 'IncomeTaxReconciliationAtFederalStatutoryIncomeTaxRate']

h1list=[
 'OperatingIncomeLoss',
 'NetIncomeLoss',
 'Revenues',
 'RevenueFromRelatedParties',
 'TaxableIncome',
 'TaxableIncomeDomestic',
 'TaxableIncomeForeign',
 'DiscontinuedOperationIncomeLossFromDiscontinuedOperationBeforeIncomeTax',
 'IncomeTaxExpenseBenefit',
 'DeferredIncomeTaxExpenseBenefit',
 'DeferredFederalIncomeTaxExpenseBenefit',
 'DeferredForeignIncomeTaxExpenseBenefit',
 'DeferredStateAndLocalIncomeTaxExpenseBenefit',
 'CurrentIncomeTaxExpenseBenefit',
 'CurrentFederalTaxExpenseBenefit',
 'CurrentForeignTaxExpenseBenefit',
 'CurrentStateAndLocalTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefitContinuingOperations',
 'StateAndLocalIncomeTaxExpenseBenefitContinuingOperations',
 'ForeignIncomeTaxExpenseBenefitContinuingOperations',
 'DomesticIncomeTaxExpenseBenefit',
 'StateAndLocalIncomeTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefit',
 'ForeignIncomeTaxExpenseBenefit',
 'DeferredTaxLiabilities',
 'AccruedIncomeTaxes',
 'AccruedIncomeTaxesCurrent',
 'AccruedIncomeTaxesNoncurrent',
 'UnrecognizedTaxBenefits',
 'UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate',
 'IncomeTaxesPaidNet',
 'IncreaseDecreaseInAccruedIncomeTaxesPayable',
 'IncomeTaxReconciliationShareBasedCompensationExcessTaxBenefit',
 'IncomeTaxReconciliationAtFederalStatutoryIncomeTaxRate',
 'EffectiveIncomeTaxRateReconciliationDeductionsDividends',
 'EffectiveIncomeTaxRateReconciliationRepatriationOfForeignEarnings',
 'EffectiveIncomeTaxRateReconciliationDeductionsQualifiedProductionActivities',
 'EffectiveIncomeTaxRateReconciliationOtherAdjustments',
 'EffectiveIncomeTaxRateReconciliationMinorityInterestIncomeExpense',
 'EffectiveIncomeTaxRateReconciliationOtherReconcilingItems',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsOther',
 'EffectiveIncomeTaxRateReconciliationTaxExemptIncome',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsResearch',
 'EffectiveIncomeTaxRateReconciliationTaxCutsAndJobsActOf2017TransitionTaxOnAccumulatedForeignEarnings',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesStateAndLocal',
 'EffectiveIncomeTaxRateReconciliationDispositionOfBusiness',
 'EffectiveIncomeTaxRateReconciliationEquityInEarningsLossesOfUnconsolidatedSubsidiary',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpense',
 'EffectiveIncomeTaxRateReconciliationDispositionOfAssets',
 'EffectiveIncomeTaxRateReconciliationForeignIncomeTaxRateDifferential',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseMealsAndEntertainment',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsDomestic',
 'EffectiveIncomeTaxRateReconciliationTaxHolidays',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesOther',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepreciationAndAmortization',
 'EffectiveIncomeTaxRateReconciliationDeductions',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsOther',
 'EffectiveIncomeTaxRateReconciliation',
 'EffectiveIncomeTaxRateReconciliationStateAndLocalIncomeTaxes',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseImpairmentLosses',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseShareBasedCompensationCost',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsInvestment',
 'EffectiveIncomeTaxRateReconciliationChangeInDeferredTaxAssetsValuationAllowance',
 'EffectiveIncomeTaxRateReconciliationTaxCredits',
 'EffectiveIncomeTaxRateReconciliationDeductionsOther',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseLifeInsurance',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsForeign',
 'EffectiveIncomeTaxRateReconciliationPriorYearIncomeTaxes',
 'EffectiveIncomeTaxRateReconciliationChangeInEnactedTaxRate',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesDomestic',
 'EffectiveIncomeTaxRateReconciliationTaxCutsAndJobsActOf2017',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesForeign',
 'EffectiveIncomeTaxRateReconciliationTaxSettlements',
 'EffectiveIncomeTaxRateReconciliationDeductionsEmployeeStockOwnershipPlanDividends',
 'EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseRestructuringCharges',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepreciation',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsStateAndLocal',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseResearchAndDevelopment',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseOther',
 'EffectiveIncomeTaxRateReconciliationTaxContingencies',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseAmortization',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsForeign',
 'EffectiveIncomeTaxRateReconciliationDeductionsExtraterritorialIncomeExclusion',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepletion',
 'EffectiveIncomeTaxRateReconciliationShareBasedCompensationExcessTaxBenefit']
h2list=[None,'DiscontinuedOperationIncomeLossFromDiscontinuedOperationBeforeIncomeTax',
 'OperatingIncomeLoss',
 'NetIncomeLoss',
 'Revenues',
 'RevenueFromRelatedParties',
 'TaxableIncome',
 'TaxableIncomeDomestic',
 'TaxableIncomeForeign',
 'DeferredTaxLiabilities',
 'AccruedIncomeTaxes',
 'AccruedIncomeTaxesCurrent',
 'AccruedIncomeTaxesNoncurrent',
 'UnrecognizedTaxBenefits',
 'UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate']
var_incomes=['DiscontinuedOperationIncomeLossFromDiscontinuedOperationBeforeIncomeTax',
 'OperatingIncomeLoss',
 'NetIncomeLoss',
 'Revenues',
 'RevenueFromRelatedParties',
 'TaxableIncome',
 'TaxableIncomeDomestic',
 'TaxableIncomeForeign']
var_tax_cash=['IncomeTaxesPaidNet', 'IncreaseDecreaseInAccruedIncomeTaxesPayable']
var_benefit_other=['TaxCutsAndJobsActOf2017IncompleteAccountingChangeInTaxRateDeferredTaxLiabilityProvisionalIncomeTaxBenefit',
 'TaxCutsAndJobsActOf2017IncompleteAccountingChangeInTaxRateDeferredTaxLiabilityExistingIncomeTaxBenefit',
 'TaxCutsAndJobsActOf2017ChangeInTaxRateDeferredTaxLiabilityIncomeTaxBenefit',
 'TaxCutsAndJobsActOf2017ChangeInTaxRateIncomeTaxExpenseBenefit',
 'TaxCutsAndJobsActOf2017IncomeTaxExpenseBenefit',
 'TaxBenefitArisingFromPreviouslyUnrecognisedTaxLossTaxCreditOrTemporaryDifferenceOfPriorPeriodUsedToReduceCurrentTaxExpense',
 'TaxBenefitArisingFromPreviouslyUnrecognisedTaxLossTaxCreditOrTemporaryDifferenceOfPriorPeriodUsedToReduceDeferredTaxExpense',
 'AffordableHousingTaxCreditsAndOtherTaxBenefitsAmount']
var_tax_expense=['IncomeTaxExpenseBenefit',
 'DeferredIncomeTaxExpenseBenefit',
 'DeferredFederalIncomeTaxExpenseBenefit',
 'DeferredForeignIncomeTaxExpenseBenefit',
 'DeferredStateAndLocalIncomeTaxExpenseBenefit',
 'CurrentIncomeTaxExpenseBenefit',
 'CurrentFederalTaxExpenseBenefit',
 'CurrentForeignTaxExpenseBenefit',
 'CurrentStateAndLocalTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefitContinuingOperations',
 'StateAndLocalIncomeTaxExpenseBenefitContinuingOperations',
 'ForeignIncomeTaxExpenseBenefitContinuingOperations',
 'DomesticIncomeTaxExpenseBenefit',
 'StateAndLocalIncomeTaxExpenseBenefit',
 'FederalIncomeTaxExpenseBenefit',
 'ForeignIncomeTaxExpenseBenefit']
var_tax_bs=['DeferredTaxLiabilities',
 'AccruedIncomeTaxes',
 'AccruedIncomeTaxesCurrent',
 'AccruedIncomeTaxesNoncurrent',
 'UnrecognizedTaxBenefits',
 'UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate']
var_recon_rates=['EffectiveIncomeTaxRateReconciliationChangeInDeferredTaxAssetsValuationAllowance',
 'EffectiveIncomeTaxRateReconciliationChangeInEnactedTaxRate',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseLifeInsurance',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseResearchAndDevelopment',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsInvestment',
 'EffectiveIncomeTaxRateReconciliationEquityInEarningsLossesOfUnconsolidatedSubsidiary',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsForeign',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseMealsAndEntertainment',
 'EffectiveIncomeTaxRateReconciliationDeductions',
 'EffectiveIncomeTaxRateReconciliationTaxCutsAndJobsActOf2017TransitionTaxOnAccumulatedForeignEarnings',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesStateAndLocal',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpense',
 'EffectiveIncomeTaxRateReconciliationForeignIncomeTaxRateDifferential',
 'EffectiveIncomeTaxRateReconciliationDeductionsEmployeeStockOwnershipPlanDividends',
 'EffectiveIncomeTaxRateReconciliationMinorityInterestIncomeExpense',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesOther',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesForeign',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseShareBasedCompensationCost',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepreciation',
 'EffectiveIncomeTaxRateReconciliationStateAndLocalIncomeTaxes',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsDomestic',
 'EffectiveIncomeTaxRateReconciliationDeductionsQualifiedProductionActivities',
 'EffectiveIncomeTaxRateReconciliationDeductionsExtraterritorialIncomeExclusion',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseImpairmentLosses',
 'EffectiveIncomeTaxRateReconciliationTaxCredits',
 'EffectiveIncomeTaxRateReconciliationTaxHolidays',
 'EffectiveIncomeTaxRateReconciliationDispositionOfBusiness',
 'EffectiveIncomeTaxRateReconciliationTaxContingencies',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepreciationAndAmortization',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsOther',
 'EffectiveIncomeTaxRateReconciliationDeductionsOther',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseDepletion',
 'EffectiveIncomeTaxRateReconciliation',
 'EffectiveIncomeTaxRateReconciliationPriorYearIncomeTaxes',
 'EffectiveIncomeTaxRateReconciliationDispositionOfAssets',
 'EffectiveIncomeTaxRateReconciliationAtFederalStatutoryIncomeTaxRate',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseRestructuringCharges',
 'EffectiveIncomeTaxRateReconciliationDeductionsDividends',
 'EffectiveIncomeTaxRateReconciliationTaxContingenciesDomestic',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseAmortization',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsStateAndLocal',
 'EffectiveIncomeTaxRateReconciliationTaxSettlements',
 'EffectiveIncomeTaxRateReconciliationOtherAdjustments',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsForeign',
 'EffectiveIncomeTaxRateReconciliationTaxCreditsResearch',
 'EffectiveIncomeTaxRateReconciliationRepatriationOfForeignEarnings',
 'EffectiveIncomeTaxRateReconciliationTaxExemptIncome',
 'EffectiveIncomeTaxRateReconciliationTaxSettlementsOther',
 'EffectiveIncomeTaxRateReconciliationOtherReconcilingItems',
 'EffectiveIncomeTaxRateReconciliationNondeductibleExpenseOther',
 'EffectiveIncomeTaxRateReconciliationTaxCutsAndJobsActOf2017',
 'EffectiveIncomeTaxRateReconciliationShareBasedCompensationExcessTaxBenefit']
var_recon_amounts=['IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance',
 'IncomeTaxReconciliationChangeInEnactedTaxRate',
 'IncomeTaxReconciliationNondeductibleExpenseLifeInsurance',
 'IncomeTaxReconciliationNondeductibleExpenseResearchAndDevelopment',
 'IncomeTaxReconciliationTaxCreditsInvestment',
 'IncomeTaxReconciliationEquityInEarningsLossesOfUnconsolidatedSubsidiary',
 'IncomeTaxReconciliationTaxSettlementsForeign',
 'IncomeTaxReconciliationNondeductibleExpenseMealsAndEntertainment',
 'IncomeTaxReconciliationDeductions',
 'IncomeTaxReconciliationTaxCutsAndJobsActOf2017TransitionTaxOnAccumulatedForeignEarnings',
 'IncomeTaxReconciliationTaxContingenciesStateAndLocal',
 'IncomeTaxReconciliationNondeductibleExpense',
 'IncomeTaxReconciliationForeignIncomeTaxRateDifferential',
 'IncomeTaxReconciliationDeductionsEmployeeStockOwnershipPlanDividends',
 'IncomeTaxReconciliationMinorityInterestIncomeExpense',
 'IncomeTaxReconciliationTaxContingenciesOther',
 'IncomeTaxReconciliationTaxContingenciesForeign',
 'IncomeTaxReconciliationNondeductibleExpenseShareBasedCompensationCost',
 'IncomeTaxReconciliationNondeductibleExpenseDepreciation',
 'IncomeTaxReconciliationStateAndLocalIncomeTaxes',
 'IncomeTaxReconciliationTaxSettlementsDomestic',
 'IncomeTaxReconciliationDeductionsQualifiedProductionActivities',
 'IncomeTaxReconciliationDeductionsExtraterritorialIncomeExclusion',
 'IncomeTaxReconciliationNondeductibleExpenseImpairmentLosses',
 'IncomeTaxReconciliationTaxCredits',
 'IncomeTaxReconciliationTaxHolidays',
 'IncomeTaxReconciliationDispositionOfBusiness',
 'IncomeTaxReconciliationTaxContingencies',
 'IncomeTaxReconciliationNondeductibleExpenseDepreciationAndAmortization',
 'IncomeTaxReconciliationTaxCreditsOther',
 'IncomeTaxReconciliationDeductionsOther',
 'IncomeTaxReconciliationNondeductibleExpenseDepletion',
 'IncomeTaxReconciliation',
 'IncomeTaxReconciliationPriorYearIncomeTaxes',
 'IncomeTaxReconciliationDispositionOfAssets',
 'IncomeTaxReconciliationAtFederalStatutoryIncomeTaxRate',
 'IncomeTaxReconciliationNondeductibleExpenseRestructuringCharges',
 'IncomeTaxReconciliationDeductionsDividends',
 'IncomeTaxReconciliationTaxContingenciesDomestic',
 'IncomeTaxReconciliationNondeductibleExpenseAmortization',
 'IncomeTaxReconciliationTaxSettlementsStateAndLocal',
 'IncomeTaxReconciliationTaxSettlements',
 'IncomeTaxReconciliationOtherAdjustments',
 'IncomeTaxReconciliationTaxCreditsForeign',
 'IncomeTaxReconciliationTaxCreditsResearch',
 'IncomeTaxReconciliationRepatriationOfForeignEarnings',
 'IncomeTaxReconciliationTaxExemptIncome',
 'IncomeTaxReconciliationTaxSettlementsOther',
 'IncomeTaxReconciliationOtherReconcilingItems',
 'IncomeTaxReconciliationNondeductibleExpenseOther',
 'IncomeTaxReconciliationTaxCutsAndJobsActOf2017',
 'IncomeTaxReconciliationShareBasedCompensationExcessTaxBenefit']

############### INDEX #######################
    
@app.route('/')
def index():
    return render_template('index.html')

################# EXPLORER ###################

@app.route('/explorer')
def explorer():

    # Get request to read in form entries
    siclist = request.args.getlist('sic')
    yearlist = request.args.getlist('year')
    s1=request.args.get('s1','IncomeTaxExpenseBenefit')
    s2=request.args.get('s2','TaxableIncome')
    h1=request.args.get('h1','Revenues')
    h2=request.args.get('h2')
    tic=request.args.get('ticker')
    
    # Build yearlist query string
    joiner='&yearlist='
    yearquery=joiner[1:]+joiner.join(yearlist)
    # Build siclist query string
    joiner='&siclist='
    sicquery=joiner[1:]+joiner.join(siclist)
    
    chart=f'explorer.json?s1={s1}&s2={s2}&h1={h1}&h2={h2}&{sicquery}&{yearquery}&ticker={tic}' 
    return render_template('explorer.html',chart=chart,s1=s1,s2=s2,s1list=slist,s2list=slist,h1list=h1list,h2list=h2list)

@app.route('/explorer.json')
def explorer_json():
    
    # Load needed files
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    
    # SIC code and year selection - checklists:
    years = request.args.getlist('yearlist')
    years=[int(y) for y in years]         
    sicselect = request.args.getlist('siclist')

    # Variable selection
    xscat=request.args.get('s1','AccruedIncomeTaxes')
    yscat=request.args.get('s2','TaxableIncome')
    histnum=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    histbase=request.args.get('h2',None)
    if histbase=='None':
        histbase=None
    tic=request.args.get('ticker',None) #User input

    #Obtain cik for selected ticker:
    if tic=='':
        ticik=None
    else:
        try:
            ticik=tickers[tickers['ticker']==tic].index.values[0]
        except:
            ticik=None

    # Generate all selected sics
    sics000=[]
    sics=[]
    count=0 #Counter for broad categories
    for s in sicselect:
        if s=='**':
            sics000.extend(list(range(0,10)))
            count=10
        if (s[-1]=='*') & (s[0]!='*'):
            sics000.append(int(s[0]))
            count+=1
        if s[-1]!='*':
            sics.append(int(s))


    t['sic00']=t['sic']//100
    t['sic000']=t['sic']//1000
    setselect=(t.index.get_level_values('year').isin(years) & ((t.index.get_level_values('cik')==ticik) | t['sic000'].isin(sics000) | t['sic00'].isin(sics)))

    # Create dataset to be inserted in Altair
    if histbase!=None:
        data_hist=t.loc[setselect,list(set([('value',xscat),('value',yscat),('value',histnum),('value',histbase),('month',histnum),('month',histbase)]))].copy()
        data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
        data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)    
    if histbase==None:
        data_hist=t.loc[setselect,list(set([('value',xscat),('value',yscat),('value',histnum),('month',histnum)]))].copy()
        data_hist[('','hist_match')]=t[('month',histnum)].notnull()
        data_hist=data_hist.drop([('month',histnum)],axis=1)

    # Drop 0 level and add sic codes and names:
    data_hist=data_hist.droplevel(axis=1,level=0)
    data_hist=data_hist.merge(dill.load(open('static/sic_codes.pkl','rb')),how='left',left_index=True,right_index=True)

    # Define variables to be aggregated:
    h1=tag2label[histnum]
    if histbase!=None:
        h2=tag2label[histbase]
    hy='Fiscal Years (histogram)'
    s1=tag2label[xscat]
    s2=tag2label[yscat]
    sy='Fiscal Years (scatter)'
    if histbase!=None:
        hvar=h1+' Per '+h2
    else:
        hvar=h1
    data_hist['scat_match']=data_hist[xscat].notnull() & data_hist[yscat].notnull()
    data_hist.loc[data_hist['hist_match'],h1]=data_hist[histnum]
    if histbase!=None:
        data_hist.loc[data_hist['hist_match'],h2]=data_hist[histbase]
    data_hist.loc[data_hist['scat_match'],s1]=data_hist[xscat]
    data_hist.loc[data_hist['scat_match'],s2]=data_hist[yscat]
    data_hist['yearc']=data_hist.index.get_level_values('year').astype('str')
    data_hist.loc[data_hist['scat_match'],sy]=data_hist['yearc']
    data_hist.loc[data_hist['hist_match'],hy]=data_hist['yearc']

    # Aggregate years:
    data_hist_sy=data_hist.loc[data_hist[sy].notnull(),sy].to_frame().groupby('cik')[sy].agg(lambda x: '; '.join(x))
    data_hist_hy=data_hist.loc[data_hist[hy].notnull(),hy].to_frame().groupby('cik')[hy].agg(lambda x: '; '.join(x))
    # Sort to pick latest company name and sic code classification:
    data_hist=data_hist.sort_values(['cik','year'],ascending=[True,False])
    if histbase!=None:
            datahs=data_hist.groupby('cik').agg({h1:'sum',h2:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    else:
            datahs=data_hist.groupby('cik').agg({h1:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    datahs.loc[datahs['scat_match']==0,[s1,s2]]=None
    datahs.loc[datahs['hist_match']==0,hvar]=None
    #Remove companies from set with no data
    datahs=datahs[datahs['scat_match']+datahs['hist_match']>0]
    #Define historgram variable:
    if histbase!=None:
        datahs[hvar]=datahs[h1]/datahs[h2]
    else:
        datahs[hvar]=datahs[h1]
    #Labels
    #Add fiscal year labels:
    datahs=datahs.merge(data_hist_sy,how='left',left_index=True,right_index=True)
    datahs=datahs.merge(data_hist_hy,how='left',left_index=True,right_index=True)
    #Add sic label and coding needed for color classication:
    if count>2:
        datahs['SICcode']=(datahs['sic']//1000)*1000
    else:
        datahs['SICcode']=(datahs['sic']//100)*100 
    datahs['SICcode']=datahs['SICcode'].astype('int')
    datahs['sic']=datahs['sic'].map('{:.0f}'.format)
    #Add string formatted labels:
    s1label='X value'
    s2label='Y value'
    hvarlabel='Histogram value'
    def formatlabel(df,var,label):
        if df[var].mean()>1:
            df[label]=df[var].map(lambda x: "${:,.0f}".format(x))
        if df[var].mean()<1:
            df[label]=df[var].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    formatlabel(datahs,s1,s1label)
    formatlabel(datahs,s2,s2label)
    if histbase!=None:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "{:,.2f}".format(x))
    elif datahs[hvar].mean()>1:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "${:,.0f}".format(x))
    else:
        datahs[hvarlabel]=datahs[hvar].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    datahs=datahs.rename(columns={'sic':'SIC code','name':'Company name'})

    # Separate data for highlighted point:
    datapt=datahs[datahs.index==ticik]

    # ALTAIR Chart

    xscale='linear'
    yscale='linear'
    hscale='linear'
    size_selector = alt.selection_multi(encodings=['x'], empty='all')
    scatter_selector = alt.selection(type='interval', encodings=['x','y'], empty='all')

    point = alt.Chart(datapt, width = 600, height=350).mark_point(filled=True,size=100).encode(
        alt.X(s1,scale=alt.Scale(type=xscale)),
        alt.Y(s2,scale=alt.Scale(type=yscale)),
      color=alt.value('red'),tooltip=['Company name','SIC code',s1label,s2label,sy,hvarlabel,hy])

    scatter = alt.Chart(datahs, width = 600, height=350).mark_point().encode(
        alt.X(s1,scale=alt.Scale(type=xscale)),
        alt.Y(s2,scale=alt.Scale(type=yscale)),
        color = alt.condition(size_selector | scatter_selector, "SICcode:N", alt.value("lightgray")),
        tooltip=['Company name','SIC code',s1label,s2label,sy,hvarlabel,hy]
    ).add_selection(scatter_selector).interactive()

    size_hist = alt.Chart(datahs, width=600, height=200).mark_bar().encode(
        alt.X(f'{hvar}:Q',bin=alt.Bin(maxbins=16),scale=alt.Scale(type=hscale)),
        y = "count()",
        color = alt.condition(size_selector , alt.value("royalblue"), alt.value("green"))
    ).transform_filter(
        scatter_selector
    ).add_selection(size_selector)
    
    plot=(scatter + point) & size_hist
    
    return plot.to_json()
    


################# EXPLORE SICS ###################

@app.route('/exploresics')
def exploresics():

    # Get request to read in form entries
    siclist = request.args.getlist('sic')
    yearlist = request.args.getlist('year')
    s1=request.args.get('s1','IncomeTaxExpenseBenefit')
    s2=request.args.get('s2','TaxableIncome')
    h1=request.args.get('h1','Revenues')
    h2=request.args.get('h2')
    
    # Build yearlist query string
    joiner='&yearlist='
    yearquery=joiner[1:]+joiner.join(yearlist)
    # Build siclist query string
    joiner='&siclist='
    sicquery=joiner[1:]+joiner.join(siclist)
    
    chart1=f'exploresics1.json?s1={s1}&s2={s2}&h1={h1}&h2={h2}&{sicquery}&{yearquery}' 
    chart2=f'exploresics2.json?s1={s1}&s2={s2}&h1={h1}&h2={h2}&{sicquery}&{yearquery}' 
    return render_template('exploresics.html',chart1=chart1,chart2=chart2,s1=s1,s2=s2,s1list=slist,s2list=slist,h1list=h1list,h2list=h2list)


@app.route('/exploresics1.json')
def exploresics1_json():
    
    # Load needed files
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    dictsic=dill.load(open('static/dictsic.pkl','rb'))
    
    # SIC code and year selection - checklists:
    years = request.args.getlist('yearlist')
    years=[int(y) for y in years]         
    sicselect = request.args.getlist('siclist')
    

    # Variable selection
    xscat=request.args.get('s1','AccruedIncomeTaxes')
    yscat=request.args.get('s2','TaxableIncome')
    histnum=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    histbase=request.args.get('h2',None)
    if histbase=='None':
        histbase=None

    # Generate all selected sics
    sics000=[]
    for s in sicselect:
        if s=='**':
            sics000.extend(list(range(0,10)))
        if (s[-1]=='*') & (s[0]!='*'):
            sics000.append(int(s[0]))

    t['sic000']=t['sic']//1000
    setselect=(t.index.get_level_values('year').isin(years) & t['sic000'].isin(sics000))

    # Create dataset to be inserted in Altair
    if histbase!=None:
        data_hist=t.loc[setselect,[('value',xscat),('value',yscat),('value',histnum),('value',histbase),('month',histnum),('month',histbase)]].copy()
        data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
        data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)    
    if histbase==None:
        data_hist=t.loc[setselect,[('value',xscat),('value',yscat),('value',histnum),('month',histnum)]].copy()
        data_hist[('','hist_match')]=t[('month',histnum)].notnull()
        data_hist=data_hist.drop([('month',histnum)],axis=1)

    # Drop 0 level and add sic codes and names:
    data_hist=data_hist.droplevel(axis=1,level=0)
    data_hist=data_hist.merge(dill.load(open(f'static/sic_codes.pkl','rb')),how='left',left_index=True,right_index=True)

    # Define variables to be aggregated:
    h1=tag2label[histnum]
    if histbase!=None:
        h2=tag2label[histbase]
    hy='Fiscal Years (histogram)'
    s1=tag2label[xscat]
    s2=tag2label[yscat]
    sy='Fiscal Years (scatter)'
    if histbase!=None:
        hvar=h1+' Per '+h2
    else:
        hvar=h1
    data_hist['scat_match']=data_hist[xscat].notnull() & data_hist[yscat].notnull()
    data_hist.loc[data_hist['hist_match'],h1]=data_hist[histnum]
    if histbase!=None:
        data_hist.loc[data_hist['hist_match'],h2]=data_hist[histbase]
    data_hist.loc[data_hist['scat_match'],s1]=data_hist[xscat]
    data_hist.loc[data_hist['scat_match'],s2]=data_hist[yscat]
    data_hist['yearc']=data_hist.index.get_level_values('year').astype('str')
    data_hist.loc[data_hist['scat_match'],sy]=data_hist['yearc']
    data_hist.loc[data_hist['hist_match'],hy]=data_hist['yearc']

    # Aggregate years:
    data_hist_sy=data_hist.loc[data_hist[sy].notnull(),sy].to_frame().groupby('cik')[sy].agg(lambda x: '; '.join(x))
    data_hist_hy=data_hist.loc[data_hist[hy].notnull(),hy].to_frame().groupby('cik')[hy].agg(lambda x: '; '.join(x))
    # Sort to pick latest company name and sic code classification:
    data_hist=data_hist.sort_values(['cik','year'],ascending=[True,False])
    if histbase!=None:
        datahs=data_hist.groupby('cik').agg({h1:'sum',h2:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    else:
        datahs=data_hist.groupby('cik').agg({h1:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    datahs.loc[datahs['scat_match']==0,[s1,s2]]=None
    datahs.loc[datahs['hist_match']==0,hvar]=None
    #Remove companies from set with no data
    datahs=datahs[datahs['scat_match']+datahs['hist_match']>0]
    #Define historgram variable:
    if histbase!=None:
        datahs[hvar]=datahs[h1]/datahs[h2]
    else:
        datahs[hvar]=datahs[h1]
    
    #Labels
    #Add fiscal year labels:
    datahs=datahs.merge(data_hist_sy,how='left',left_index=True,right_index=True)
    datahs=datahs.merge(data_hist_hy,how='left',left_index=True,right_index=True)
    #Add sic label and coding needed for color classication:
    datahs['SIC codes']=(datahs['sic']//1000)*1000
    datahs['SIC codes']=datahs['SIC codes'].map(lambda x: dictsic[x]) 
    datahs['sic']=datahs['sic'].map('{:.0f}'.format)
    #Add string formatted labels:
    s1label='X value'
    s2label='Y value'
    hvarlabel='Histogram value'
    def formatlabel(df,var,label):
        if df[var].mean()>1:
            df[label]=df[var].map(lambda x: "${:,.0f}".format(x))
        if df[var].mean()<1:
            df[label]=df[var].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    formatlabel(datahs,s1,s1label)
    formatlabel(datahs,s2,s2label)
    if histbase!=None:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "{:,.2f}".format(x))
    elif datahs[hvar].mean()>1:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "${:,.0f}".format(x))
    else:
        datahs[hvarlabel]=datahs[hvar].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    datahs=datahs.rename(columns={'sic':'SIC code','name':'Company name'})
    
    #ALTAIR Graph

    xscale='linear'
    yscale='linear'
    hscale='linear'

    scatter = alt.Chart(datahs, width = 500).mark_point().encode(
        alt.X(s1,scale=alt.Scale(type=xscale)),
        alt.Y(s2,scale=alt.Scale(type=yscale),axis=alt.Axis(title=None)),
        color = "SIC codes:N",
        tooltip=['Company name','SIC code',s1label,s2label,sy,hvarlabel,hy]
    ).interactive()

    plot1=scatter.facet(row=alt.Row("SIC codes:N",title=s2))

    return plot1.to_json()

@app.route('/exploresics2.json')
def exploresics2_json():
    
    # Load needed files
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    dictsic=dill.load(open('static/dictsic.pkl','rb'))
    
    # SIC code and year selection - checklists:
    years = request.args.getlist('yearlist')
    years=[int(y) for y in years]         
    sicselect = request.args.getlist('siclist')
    

    # Variable selection
    xscat=request.args.get('s1','AccruedIncomeTaxes')
    yscat=request.args.get('s2','TaxableIncome')
    histnum=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    histbase=request.args.get('h2',None)
    if histbase=='None':
        histbase=None

    # Generate all selected sics
    sics000=[]
    for s in sicselect:
        if s=='**':
            sics000.extend(list(range(0,10)))
        if (s[-1]=='*') & (s[0]!='*'):
            sics000.append(int(s[0]))

    t['sic000']=t['sic']//1000
    setselect=(t.index.get_level_values('year').isin(years) & t['sic000'].isin(sics000))

    # Create dataset to be inserted in Altair
    if histbase!=None:
        data_hist=t.loc[setselect,[('value',xscat),('value',yscat),('value',histnum),('value',histbase),('month',histnum),('month',histbase)]].copy()
        data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
        data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)    
    if histbase==None:
        data_hist=t.loc[setselect,[('value',xscat),('value',yscat),('value',histnum),('month',histnum)]].copy()
        data_hist[('','hist_match')]=t[('month',histnum)].notnull()
        data_hist=data_hist.drop([('month',histnum)],axis=1)

    # Drop 0 level and add sic codes and names:
    data_hist=data_hist.droplevel(axis=1,level=0)
    data_hist=data_hist.merge(dill.load(open(f'static/sic_codes.pkl','rb')),how='left',left_index=True,right_index=True)

    # Define variables to be aggregated:
    h1=tag2label[histnum]
    if histbase!=None:
        h2=tag2label[histbase]
    hy='Fiscal Years (histogram)'
    s1=tag2label[xscat]
    s2=tag2label[yscat]
    sy='Fiscal Years (scatter)'
    if histbase!=None:
        hvar=h1+' Per '+h2
    else:
        hvar=h1
    data_hist['scat_match']=data_hist[xscat].notnull() & data_hist[yscat].notnull()
    data_hist.loc[data_hist['hist_match'],h1]=data_hist[histnum]
    if histbase!=None:
        data_hist.loc[data_hist['hist_match'],h2]=data_hist[histbase]
    data_hist.loc[data_hist['scat_match'],s1]=data_hist[xscat]
    data_hist.loc[data_hist['scat_match'],s2]=data_hist[yscat]
    data_hist['yearc']=data_hist.index.get_level_values('year').astype('str')
    data_hist.loc[data_hist['scat_match'],sy]=data_hist['yearc']
    data_hist.loc[data_hist['hist_match'],hy]=data_hist['yearc']

    # Aggregate years:
    data_hist_sy=data_hist.loc[data_hist[sy].notnull(),sy].to_frame().groupby('cik')[sy].agg(lambda x: '; '.join(x))
    data_hist_hy=data_hist.loc[data_hist[hy].notnull(),hy].to_frame().groupby('cik')[hy].agg(lambda x: '; '.join(x))
    # Sort to pick latest company name and sic code classification:
    data_hist=data_hist.sort_values(['cik','year'],ascending=[True,False])
    if histbase!=None:
        datahs=data_hist.groupby('cik').agg({h1:'sum',h2:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    else:
        datahs=data_hist.groupby('cik').agg({h1:'sum',s1:'sum',s2:'sum','scat_match':'sum','hist_match':'sum','sic':'first','name':'first'})
    datahs.loc[datahs['scat_match']==0,[s1,s2]]=None
    datahs.loc[datahs['hist_match']==0,hvar]=None
    #Remove companies from set with no data
    datahs=datahs[datahs['scat_match']+datahs['hist_match']>0]
    #Define historgram variable:
    if histbase!=None:
        datahs[hvar]=datahs[h1]/datahs[h2]
    else:
        datahs[hvar]=datahs[h1]
    
    #Labels
    #Add fiscal year labels:
    datahs=datahs.merge(data_hist_sy,how='left',left_index=True,right_index=True)
    datahs=datahs.merge(data_hist_hy,how='left',left_index=True,right_index=True)
    #Add sic label and coding needed for color classication:
    datahs['SIC codes']=(datahs['sic']//1000)*1000
    datahs['SIC codes']=datahs['SIC codes'].map(lambda x: dictsic[x]) 
    datahs['sic']=datahs['sic'].map('{:.0f}'.format)
    #Add string formatted labels:
    s1label='X value'
    s2label='Y value'
    hvarlabel='Histogram value'
    def formatlabel(df,var,label):
        if df[var].mean()>1:
            df[label]=df[var].map(lambda x: "${:,.0f}".format(x))
        if df[var].mean()<1:
            df[label]=df[var].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    formatlabel(datahs,s1,s1label)
    formatlabel(datahs,s2,s2label)
    if histbase!=None:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "{:,.2f}".format(x))
    elif datahs[hvar].mean()>1:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "${:,.0f}".format(x))
    else:
        datahs[hvarlabel]=datahs[hvar].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    datahs=datahs.rename(columns={'sic':'SIC code','name':'Company name'})
    
    #ALTAIR Graph

    xscale='linear'
    yscale='linear'
    hscale='linear'


    size_hist = alt.Chart(datahs, width=400, height=200).mark_bar().encode(
        alt.X(f'{hvar}:Q',bin=alt.Bin(maxbins=14),scale=alt.Scale(type=hscale)),
        y = "count()",
        color = alt.value("royalblue")
    )

    plot2=size_hist.facet(row="SIC codes:N")

    return plot2.to_json()


################# EXPLORE SIZE ###################

@app.route('/exploresize')
def exploresize():

    # Get request to read in form entries
    qlist = request.args.getlist('q')
    yearlist = request.args.getlist('year')
    h1=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    h2=request.args.get('h2')
    
    # Build yearlist query string
    joiner='&yearlist='
    yearquery=joiner[1:]+joiner.join(yearlist)
    # Build siclist query string
    joiner='&qlist='
    qquery=joiner[1:]+joiner.join(qlist)
    
    chart=f'exploresize.json?h1={h1}&h2={h2}&{qquery}&{yearquery}' 
    h1list_size=h1list[:h1list.index('Revenues')]+h1list[h1list.index('Revenues')+1:]
    return render_template('exploresize.html',chart=chart,h1list=h1list_size,h2list=h2list)


@app.route('/exploresize.json')
def exploresize_json():
    
    # Load needed files
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    dictsic=dill.load(open('static/dictsic.pkl','rb'))
    
    # quantile and year selection - checklists:
    years = request.args.getlist('yearlist')
    years=[int(y) for y in years]         
    qselect = request.args.getlist('qlist')
    qselect=[int(q) for q in qselect] 
    

    # Variable selection
    histnum=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    histbase=request.args.get('h2',None)
    if histbase=='None':
        histbase=None


    t['sic000']=t['sic']//1000
    setselect=(t.index.get_level_values('year').isin(years))

    # Create dataset to be inserted in Altair
    if (histbase!=None) & (histbase!='Revenues'):
        data_hist=t.loc[setselect,[('value','Revenues'),('value',histnum),('value',histbase),('month',histnum),('month',histbase)]].copy()
        data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
        data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)    
    if histbase==None:
        data_hist=t.loc[setselect,[('value','Revenues'),('value',histnum),('month',histnum)]].copy()
        data_hist[('','hist_match')]=t[('month',histnum)].notnull()
        data_hist=data_hist.drop([('month',histnum)],axis=1)
    if histbase=='Revenues':
        data_hist=t.loc[setselect,[('value',histnum),('value',histbase),('month',histnum),('month',histbase)]].copy()
        data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
        data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)

    # Drop 0 level and add sic codes and names:
    data_hist=data_hist.droplevel(axis=1,level=0)
    data_hist=data_hist.merge(dill.load(open(f'static/sic_codes.pkl','rb')),how='left',left_index=True,right_index=True)

    # Define variables to be aggregated:
    h1=tag2label[histnum]
    if histbase!=None:
        h2=tag2label[histbase]
    hy='Fiscal Years (histogram)'
    if histbase!=None:
        hvar=h1+' Per '+h2
    else:
        hvar=h1

    data_hist.loc[data_hist['hist_match'],h1]=data_hist[histnum]
    if histbase!=None:
        data_hist.loc[data_hist['hist_match'],h2]=data_hist[histbase]

    data_hist['yearc']=data_hist.index.get_level_values('year').astype('str')
    data_hist.loc[data_hist['hist_match'],hy]=data_hist['yearc']
  
    # Aggregate years:
    data_hist_hy=data_hist.loc[data_hist[hy].notnull(),hy].to_frame().groupby('cik')[hy].agg(lambda x: '; '.join(x))

    # Sort to pick latest company name and sic code classification:
    data_hist=data_hist.sort_values(['cik','year'],ascending=[True,False])
    if histbase!=None:
        datahs=data_hist.groupby('cik').agg({h1:'sum',h2:'sum','hist_match':'sum','sic':'first','Revenues':'first','name':'first'})
    else:
        datahs=data_hist.groupby('cik').agg({h1:'sum','hist_match':'sum','sic':'first','Revenues':'first','name':'first'})
    datahs.loc[datahs['hist_match']==0,hvar]=None
    # Assign size quantiles by latest revenue figure:
    quantiles = pd.qcut(datahs['Revenues'], 10, labels=False)
    datahs = datahs.assign(quantile=quantiles.values) 
    datahs=datahs[datahs['quantile'].isin(qselect)]
    #Remove companies from set with no data
    datahs=datahs[datahs['hist_match']>0]
    #Define historgram variable:
    if histbase!=None:
        datahs[hvar]=datahs[h1]/datahs[h2]
    else:
        datahs[hvar]=datahs[h1]
    
    #Labels
    #Add fiscal year labels:
    datahs=datahs.merge(data_hist_hy,how='left',left_index=True,right_index=True)
    #Add sic label and coding needed for color classication:
    datahs['SIC codes']=(datahs['sic']//1000)*1000
    datahs['SIC codes']=datahs['SIC codes'].map(lambda x: dictsic[x]) 
    datahs['sic']=datahs['sic'].map('{:.0f}'.format)
    #Add string formatted labels:
    s1label='X value'
    s2label='Y value'
    hvarlabel='Histogram value'

    if histbase!=None:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "{:,.2f}".format(x))
    elif datahs[hvar].mean()>1:
        datahs[hvarlabel]=datahs[hvar].map(lambda x: "${:,.0f}".format(x))
    else:
        datahs[hvarlabel]=datahs[hvar].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
    datahs=datahs.rename(columns={'sic':'SIC code','name':'Company name'})
    
    #ALTAIR Graph

    xscale='linear'
    yscale='linear'
    hscale='linear'

    size_hist = alt.Chart(datahs, width=400, height=200).mark_bar().encode(
        alt.X(f'{hvar}:Q',bin=alt.Bin(maxbins=14),scale=alt.Scale(type=hscale)),
        y = "count()",
        color = alt.value("royalblue")
    )

    plot=size_hist.facet(row="quantile:N")

    return plot.to_json()
    
    
################# RECONCILE ###################

@app.route('/reconciliation')
def reconciliation():
    dictsic=dill.load(open('static/dictsic.pkl','rb'))
    
    # Get request to read in form entries
    siclist = request.args.getlist('sic')
    yearlist = request.args.getlist('year')
    minfreq=request.args.get('minfreq')
    if minfreq=='':
        minfreq=0
    else:
        try:
            minfreq=float(minfreq)
        except:
            minfreq=0

    # Build yearlist query string
    joiner='&yearlist='
    yearquery=joiner[1:]+joiner.join(yearlist)
    # Build siclist query string
    joiner='&siclist='
    sicquery=joiner[1:]+joiner.join(siclist)
    if '**' not in siclist:
        sics=[dictsic[int(sic[0])*1000] for sic in siclist]
    else:
        sics='All'
    
    query=f'reconciliation.json?{sicquery}&{yearquery}&minfreq={minfreq}' 
    #df=pd.read_json(f'https://202009.tditrain.com/user/go.lazarevski@gmail.com/proxy/33507/reconciliation.json?{sicquery}&{yearquery}&minfreq={minfreq}')
    #N=len(df)
    y_axis_format=alt.Axis(labelLimit=1000,labelFontSize=12,titleFontSize=14,titleX=-6,titleY=-6,titleAlign='right',titleAngle=0)
    if minfreq>0.2:
        h=400
    elif (minfreq>0.1) & (minfreq<=0.2):
        h=600
    elif (minfreq>0.05) & (minfreq<=0.1):
        h=800
    elif minfreq==0:
        h=2500
    else:
        h=50*(50-300*minfreq)
    #y_axis_sort=alt.EncodingSortField(field='means',op='mean', order='ascending')
    p=alt.Chart(query,width = 500, height=h).mark_boxplot(size=40, extent=0.5).encode(
    x=alt.X('value:Q'),
    y=alt.Y('Reconciliation item (mean, count):O',axis=y_axis_format))    
    if siclist:
        return render_template('reconciliation.html',sics=sics,yearlist=yearlist,chart=p.to_json())
    else:
        return render_template('reconciliation.html',sics=sics,yearlist=yearlist)

    
@app.route('/reconciliation.json')
def reconciliation_json():
        
    # Load necessary files:
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    
    # Sample values:
#     years=[2018,2019]
#     sicselect=['3*','4*','5*']
#     minfreq='0.1'
    
    # User selections: SIC code, years and min freq:
    years = request.args.getlist('yearlist')
    years=[int(y) for y in years]         
    sicselect = request.args.getlist('siclist')
    minfreq=request.args.get('minfreq',None)
    if minfreq=='':
        minfreq=0
    else:
        try:
            minfreq=float(minfreq)
        except:
            minfreq=0

    # Generate all selected sics
    sics000=[]
    for s in sicselect:
        if s=='**':
            sics000.extend(list(range(0,10)))
        if (s[-1]=='*') & (s[0]!='*'):
            sics000.append(int(s[0]))

    t['sic000']=t['sic']//1000
    setselect=(t.index.get_level_values('year').isin(years) & t['sic000'].isin(sics000))

    # Create dataset to be inserted in Seabon
    rec_value_vars=[('value',var) for var in var_recon_rates]
    data_rec=t.loc[setselect,rec_value_vars].copy()
    data_rec=data_rec.droplevel(axis=1,level=0)
    # Aggregate years:
    datarc=data_rec.groupby('cik').agg('mean')
    # Drop vars below min frequency cutoff and outliers (likely errors):
    var_recon_rates_freq=var_recon_rates.copy()
    for var in var_recon_rates:
        datarc.loc[abs(datarc[var])>1,var]=None
        if datarc[var].count()<minfreq*len(datarc):
            datarc=datarc.drop(var, axis=1)
            var_recon_rates_freq.pop(var_recon_rates_freq.index(var))

    # Create labels dictionary for boxes containing mean and count values
    boxesdict={var: tag2label[var][41:-9].strip()+' ('+'{:,.1f}%'.format(datarc[var].mean()*100)+'; N='+f'{datarc[var].count()}'+')' for var in var_recon_rates_freq}

    #Create ordering index for boxplot based on labels
    ordering=datarc.mean().sort_values().reset_index()
    ordering['tag']=ordering['tag'].map(lambda x: boxesdict[x])
    ordering.set_index('tag',inplace=True)
    ordering=ordering.rename(columns={0:'means'})

    # Create boxplot
    datarc_long=datarc.melt(value_vars=var_recon_rates_freq)
    # Replace tags with labels
    datarc_long['Reconciliation item (mean, count)']=datarc_long['tag'].map(lambda x: boxesdict[x])
    
    # Sort and save as json object
    datarcm=datarc_long.merge(ordering,left_on='Reconciliation item (mean, count)', right_index=True)
    datarcm=datarcm.sort_values('means')
    
    return datarcm.to_json(orient='records')



################# GLOSSARY ###################

@app.route('/glossary')
def glossary():
    desc=dill.load(open('static/desc.pkl','rb'))
    deschtml=desc.to_html()
    return render_template('glossary.html',deschtml=deschtml)

################# FACT SHEET ###################

@app.route('/factsheet')
def factsheet():
    yearlist=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    # Get request to read in form entries
    year = request.args.get('year','')
    if year!='':
        year=int(year)
    tic=request.args.get('ticker','')
    
    # Load needed files
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    dictsic=dill.load(open('static/dictsic.pkl','rb'))
    fye=dill.load(open('static/fye_month.pkl','rb'))
    
    #Obtain cik for selected ticker:
    if tic=='':
        ticik=None
    else:
        try:
            ticik=tickers[tickers['ticker']==tic].index.values[0]
        except:
            ticik=None

    if ticik:
        # Obtain fiscal year month end info:
        fyedict={1:'January 31st',2:"February 28th",3:'March 31st',4:'April 30th',5:'May 31st',6:"June 30th",
                 7:'July 31st',8:'August 31st',9:'September 30th',10:'October 31st',11:'November 30th',12:'December 31st'}
        msg=''
        try:
            fym=fyedict[fye.loc[(fye.index.get_level_values('fy')==year) & (fye.index.get_level_values('cik')==ticik)]['fym'].values[0]]

            facts=t.loc[(t.index.get_level_values('year')==year) & (t.index.get_level_values('cik')==ticik)].T
        except:
            msg='No data available for the year selected.'
            facts_recon=None
            facts_cs=None
            facts_bs=None
            facts_income=None
            fym=''
            sic=int(t.loc[(t.index.get_level_values('cik')==ticik)]['sic'].values[0])
            name=t.loc[(t.index.get_level_values('cik')==ticik)]['name'].values[0]
        else:
            #Obtain name and SIC code
            name=facts.loc['name'].values[0,0]
            sic=int(facts.loc['sic'].values[0,0])

            # Drop unneeded levels:
            facts=facts.drop('month',level=0)
            facts=facts.drop('',level=1)
            facts=facts.droplevel(axis=1,level=0)
            facts=facts.droplevel(axis=0,level=0)

            #  Organize table
            facts=facts.reset_index()
            facts['Variable']=facts['tag'].map(lambda x:tag2label[x])
            facts=facts.dropna()

            # Income statement items
            facts_income=facts.loc[facts['tag'].isin(var_incomes)].append(facts.loc[facts['tag'].isin(var_tax_expense+var_benefit_other)])
            facts_income['Amount (USD)']=facts_income[year].map('$ {:,.0f}'.format)
            facts_income.columns.names=['']
            facts_income=facts_income[['Variable','Amount (USD)']]
            facts_income=facts_income.set_index('Variable')
            facts_income=facts_income.to_html()

            # Balance sheet items
            facts_bs=facts.loc[facts['tag'].isin(var_tax_bs)]
            facts_bs['Amount (USD)']=facts_bs[year].map('$ {:,.0f}'.format)
            facts_bs.columns.names=['']
            facts_bs=facts_bs[['Variable','Amount (USD)']]
            facts_bs=facts_bs.set_index('Variable')
            facts_bs=facts_bs.to_html()

            # Cash flow items
            facts_cs=facts.loc[facts['tag'].isin(var_tax_cash)]
            facts_cs['Amount (USD)']=facts_cs[year].map('$ {:,.0f}'.format)
            facts_cs.columns.names=['']
            facts_cs=facts_cs[['Variable','Amount (USD)']]
            facts_cs=facts_cs.set_index('Variable')
            facts_cs=facts_cs.to_html()

            # Tax rate reconciliation
            facts_recon=facts.loc[facts['tag'].isin(var_recon_rates)]
            facts_recon=facts_recon.sort_values([year],ascending=False)
            facts_recon['Tax Rate Reconciliation Item']=facts_recon['Variable'].map(lambda x:x[42:-9])
            facts_recon['item']=facts_recon['tag'].map(lambda x:x[36:])
            facts_recon['Percent (%)']=facts_recon[year].map(lambda x:100*x).map('{:.2f} %'.format)
            facts_recon=facts_recon.set_index('item')

            facts_recon2=facts.loc[facts['tag'].isin(var_recon_amounts)]
            facts_recon2['item']=facts_recon2['tag'].map(lambda x:x[23:])
            facts_recon2['Amount (USD)']=facts_recon2[year].map('$ {:,.0f}'.format)
            facts_recon2=facts_recon2[['item','Amount (USD)']]
            facts_recon2=facts_recon2.set_index('item')

            facts_recon=facts_recon.merge(facts_recon2,left_index=True,right_index=True)
            facts_recon=facts_recon.reset_index()
            facts_recon=facts_recon[['Tax Rate Reconciliation Item','Percent (%)','Amount (USD)']]
            facts_recon.columns.names=['']
            facts_recon=facts_recon.set_index('Tax Rate Reconciliation Item')  
            facts_recon=facts_recon.to_html()
    else:
        facts_recon=None
        facts_cs=None
        facts_bs=None
        facts_income=None
        name='Enter a valid company ticker'
        sic=None
        fym=None
        msg=''
    
    
    return render_template('factsheet.html',facts_income=facts_income,facts_bs=facts_bs,facts_cs=facts_cs,facts_recon=facts_recon,yearlist=yearlist,name=name,sic=sic,fym=fym,msg=msg,year=year)

################# TRENDS ###################

@app.route('/trends')
def trends():
        
    # Load necessary files:
    t=dill.load(open('static/t.pkl','rb'))
    tag2label=dill.load(open('static/tag2label.pkl','rb'))
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')


    # Get request to read in form entries
    yearlist = request.args.getlist('year')
    if 'All Available' in yearlist:
        years=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    else:
        years=[int(y) for y in yearlist]       
    
    histnum=request.args.get('h1','DomesticIncomeTaxExpenseBenefit')
    histbase=request.args.get('h2',None)
    if histbase=='None':
        histbase=None
    tic=request.args.get('ticker',None)
    #Obtain cik for selected ticker:
    if tic=='':
        ticik=None
    else:
        try:
            ticik=tickers[tickers['ticker']==tic].index.values[0]
        except:
            ticik=None  

    if yearlist and ticik:        
        setselect=(t.index.get_level_values('year').isin(years) & (t.index.get_level_values('cik')==ticik))

        # Create dataset to be inserted in Altair
        if histbase!=None:
            data_hist=t.loc[setselect,[('value',histnum),('value',histbase),('month',histnum),('month',histbase)]].copy()
            data_hist[('','hist_match')]=(t[('month',histnum)]==t[('month',histbase)])
            data_hist=data_hist.drop([('month',histnum),('month',histbase)],axis=1)    
        if histbase==None:
            data_hist=t.loc[setselect,list(set([('value',histnum),('month',histnum)]))].copy()
            data_hist[('','hist_match')]=t[('month',histnum)].notnull()
            data_hist=data_hist.drop([('month',histnum)],axis=1)

        # Drop 0 level and add company name:
        data_hist=data_hist.droplevel(axis=1,level=0)
        data_hist=data_hist.merge(dill.load(open('static/sic_codes.pkl','rb')),how='left',left_index=True,right_index=True)
        data_hist=data_hist.droplevel(axis=0,level=0)

        # Define variables to be charted:
        h1=tag2label[histnum]
        if histbase!=None:
            h2=tag2label[histbase]
        hy='Fiscal Years'
        if histbase!=None:
            hvar=h1+' Per '+h2
        else:
            hvar=h1
        data_hist.loc[data_hist['hist_match'],h1]=data_hist[histnum]
        if histbase!=None:
            data_hist.loc[data_hist['hist_match'],h2]=data_hist[histbase]
        data_hist['yearc']=data_hist.index.get_level_values('year').astype('str')
        data_hist.loc[data_hist['hist_match'],hy]=data_hist['yearc']

        # Sort years:
        data_hist=data_hist.sort_values('year',ascending=True)

        #Define trendline variable:
        if histbase!=None:
            data_hist[hvar]=data_hist[h1]/data_hist[h2]
        else:
            data_hist[hvar]=data_hist[h1]
        data_hist.loc[data_hist['hist_match']==0,hvar]=None

        #Add string formatted labels:
        hvarlabel='Trendline value'
        if histbase!=None:
            data_hist[hvarlabel]=data_hist[hvar].map(lambda x: "{:,.2f}".format(x))
        elif data_hist[hvar].mean()>1:
            data_hist[hvarlabel]=data_hist[hvar].map(lambda x: "${:,.0f}".format(x))
        else:
            data_hist[hvarlabel]=data_hist[hvar].map(lambda x:100*x).map(lambda x: "{:,.2f}%".format(x))
        
        # Plot figiure
        perc=None
        if (histbase==None) & (data_hist[hvar].mean()<=1):
            data_hist[hvar]=data_hist[hvar].map(lambda x:100*x)
            perc=True
        
        img = BytesIO()
        plt.figure(figsize=(10,6))
        plt.plot(hy,hvar,'b-',marker='o',lw=0.5,data=data_hist)
        plt.xlabel(hy)
        plt.grid(True)
        plt.suptitle(data_hist['name'].values[0])
        plt.title(hvar)
        # after plotting the data, format the labels
        current_values = plt.gca().get_yticks()
        if histbase!=None:
            plt.gca().set_yticklabels(['{:.2f}'.format(x) for x in current_values])
        elif perc==True:
            plt.gca().set_yticklabels(['{:.1f}%'.format(x) for x in current_values])
            perc=None
        else:
            plt.gca().set_yticklabels(['${:,.0f}'.format(x) for x in current_values])
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    if yearlist and ticik:
        return render_template('trends.html',h1list=h1list,h2list=h2list,plot_url=plot_url)
    else:
        return render_template('trends.html',h1list=h1list,h2list=h2list)

    
    
################# TICKERS ###################

@app.route('/tickers')
def tickers():
    #Load and merge necessary files
    t=dill.load(open('static/t.pkl','rb'))   
    tickers=pd.read_table('static/tickers.txt')
    tickers=tickers.set_index('cik')
    tickers=tickers.merge(t[['name']].groupby('cik').agg('first'),left_index=True, right_index=True)
    tickers=tickers.set_index('ticker')
    tickers=tickers.rename(columns={('name', ''):'Company name'})
    tichtml=tickers.to_html()
    return render_template('tickers.html',tichtml=tichtml)

################# ABOUT ###################

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)


