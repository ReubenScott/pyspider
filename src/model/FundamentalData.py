from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField, BooleanField, CompositeKey, \
  PrimaryKeyField, DecimalField

from src.config.env import db

# db = SqliteDatabase('E:/Documents/market.db')
# db.connect()
# db.create_tables([CompanyOverview, IncomeStatement])


class ListingStatus(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'exchange')

  symbol = CharField()
  exchange = CharField()
  name = CharField()
  assetType = CharField()
  ipoDate = DateField()
  delistingDate = DateField()
  status = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class IPOCalendar(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'exchange')

  symbol = CharField()
  name = CharField()
  ipoDate = DateField()
  priceRangeLow = DecimalField()
  priceRangeHigh = DecimalField()
  currency = CharField()
  exchange = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class EarningsCalendar(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'fiscalDateEnding')

  symbol = CharField()
  name = CharField()
  reportDate = DateField()
  fiscalDateEnding = DateField()
  estimate = DecimalField()
  currency = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class CompanyOverview(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database

  Symbol = PrimaryKeyField()
  AssetType = CharField()
  Name = CharField()
  Description = CharField()
  CIK = CharField()
  Exchange = CharField()
  Currency = CharField()
  Country = CharField()
  Sector = CharField()
  Industry = CharField()
  Address = CharField()
  FiscalYearEnd = CharField()
  LatestQuarter = CharField()
  MarketCapitalization = CharField()
  EBITDA = CharField()
  PERatio = CharField()
  PEGRatio = CharField()
  BookValue = CharField()
  DividendPerShare = CharField()
  DividendYield = CharField()
  EPS = CharField()
  RevenuePerShareTTM = CharField()
  ProfitMargin = CharField()
  OperatingMarginTTM = CharField()
  ReturnOnAssetsTTM = CharField()
  ReturnOnEquityTTM = CharField()
  RevenueTTM = CharField()
  GrossProfitTTM = CharField()
  DilutedEPSTTM = CharField()
  QuarterlyEarningsGrowthYOY = CharField()
  QuarterlyRevenueGrowthYOY = CharField()
  AnalystTargetPrice = CharField()
  AnalystRatingStrongBuy = CharField()
  AnalystRatingBuy = CharField()
  AnalystRatingHold = CharField()
  AnalystRatingSell = CharField()
  AnalystRatingStrongSell = CharField()
  TrailingPE = CharField()
  ForwardPE = CharField()
  PriceToSalesRatioTTM = CharField()
  PriceToBookRatio = CharField()
  EVToRevenue = CharField()
  EVToEBITDA = CharField()
  Beta = CharField()
  High52Week = CharField()
  Low52Week = CharField()
  MovingAverage50Day = CharField()
  MovingAverage200Day = CharField()
  SharesOutstanding = CharField()
  DividendDate = CharField()
  ExDividendDate = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data,
      High52Week=json_data["52WeekHigh"],
      Low52Week=json_data["52WeekLow"],
      MovingAverage50Day=json_data["50DayMovingAverage"],
      MovingAverage200Day=json_data["200DayMovingAverage"],
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
      # "52WeekHigh": self.High52Week,
      # "52WeekLow": self.Low52Week,
    }


class IncomeStatement(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  grossProfit = IntegerField()
  totalRevenue = IntegerField()
  costOfRevenue = IntegerField()
  costofGoodsAndServicesSold = IntegerField()
  operatingIncome = IntegerField()
  sellingGeneralAndAdministrative = IntegerField()
  researchAndDevelopment = IntegerField()
  operatingExpenses = IntegerField()
  investmentIncomeNet = CharField()
  netInterestIncome = IntegerField()
  interestIncome = CharField()
  interestExpense = IntegerField()
  nonInterestIncome = CharField()
  otherNonOperatingIncome = IntegerField()
  depreciation = IntegerField()
  depreciationAndAmortization = IntegerField()
  incomeBeforeTax = IntegerField()
  incomeTaxExpense = IntegerField()
  interestAndDebtExpense = IntegerField()
  netIncomeFromContinuingOperations = IntegerField()
  comprehensiveIncomeNetOfTax = IntegerField()
  ebit = IntegerField()
  ebitda = IntegerField()
  netIncome = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class BalanceSheet(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  totalAssets = IntegerField()
  totalCurrentAssets = IntegerField()
  cashAndCashEquivalentsAtCarryingValue = IntegerField()
  cashAndShortTermInvestments = IntegerField()
  inventory = IntegerField()
  currentNetReceivables = CharField()
  totalNonCurrentAssets = IntegerField()
  propertyPlantEquipment = IntegerField()
  accumulatedDepreciationAmortizationPPE = CharField()
  intangibleAssets = IntegerField()
  intangibleAssetsExcludingGoodwill = IntegerField()
  goodwill = IntegerField()
  investments = CharField()
  longTermInvestments = CharField()
  shortTermInvestments = IntegerField()
  otherCurrentAssets = IntegerField()
  otherNonCurrentAssets = CharField()
  totalLiabilities = IntegerField()
  totalCurrentLiabilities = IntegerField()
  currentAccountsPayable = IntegerField()
  deferredRevenue = CharField()
  currentDebt = IntegerField()
  shortTermDebt = IntegerField()
  totalNonCurrentLiabilities = IntegerField()
  capitalLeaseObligations = CharField()
  longTermDebt = IntegerField()
  currentLongTermDebt = CharField()
  longTermDebtNoncurrent = CharField()
  shortLongTermDebtTotal = IntegerField()
  otherCurrentLiabilities = IntegerField()
  otherNonCurrentLiabilities = IntegerField()
  totalShareholderEquity = IntegerField()
  treasuryStock = IntegerField()
  retainedEarnings = IntegerField()
  commonStock = IntegerField()
  commonStockSharesOutstanding = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class CashFlow(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  operatingCashflow = IntegerField()
  paymentsForOperatingActivities = IntegerField()
  proceedsFromOperatingActivities = CharField()
  changeInOperatingLiabilities = IntegerField()
  changeInOperatingAssets = IntegerField()
  depreciationDepletionAndAmortization = IntegerField()
  capitalExpenditures = IntegerField()
  changeInReceivables = IntegerField()
  changeInInventory = IntegerField()
  profitLoss = IntegerField()
  cashflowFromInvestment = IntegerField()
  cashflowFromFinancing = IntegerField()
  proceedsFromRepaymentsOfShortTermDebt = IntegerField()
  paymentsForRepurchaseOfCommonStock = CharField()
  paymentsForRepurchaseOfEquity = CharField()
  paymentsForRepurchaseOfPreferredStock = CharField()
  dividendPayout = IntegerField()
  dividendPayoutCommonStock = IntegerField()
  dividendPayoutPreferredStock = CharField()
  proceedsFromIssuanceOfCommonStock = CharField()
  proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = IntegerField()
  proceedsFromIssuanceOfPreferredStock = CharField()
  proceedsFromRepurchaseOfEquity = IntegerField()
  proceedsFromSaleOfTreasuryStock = CharField()
  changeInCashAndCashEquivalents = CharField()
  changeInExchangeRate = CharField()
  netIncome = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class Earnings(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedDate = DateField()
  reportedEPS = DecimalField()
  estimatedEPS = DecimalField()
  surprise = DecimalField()
  surprisePercentage = DecimalField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }
