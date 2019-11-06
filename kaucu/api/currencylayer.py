import requests
from decimal import *

class CurrencyLayer:
  access_key = '54794f70a37cb8257e6a128c9295cb03'
  def exchangeRate(self, fromCurrency):
    toCurrency = 'GBP'
    if fromCurrency != 'GBP':
      endpoint = 'live'
      url = 'https://apilayer.net/api/'+endpoint+'?access_key='+self.access_key+'&currencies='+fromCurrency+'&source='+toCurrency
      req = requests.get(url)
      rate = req.json()['quotes'][toCurrency+fromCurrency]
      return round(Decimal(rate),4)
    else:
      return 1

  def exchangeRateHistoric(self, fromCurrency, date):
    toCurrency = 'GBP'
    ##date YYYY-MM-DD
    if fromCurrency != 'GBP':
      endpoint = 'historical'
      url = 'https://apilayer.net/api/'+endpoint+'?access_key='+self.access_key+'&currencies='+fromCurrency+'&source='+toCurrency+'&date='+date
      req = requests.get(url)
      rate = req.json()['quotes'][toCurrency+fromCurrency]
      return round(Decimal(rate),4)
    else:
      return 1
