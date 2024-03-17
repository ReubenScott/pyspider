#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from src.headless.kabumap import Kabumap
from src.headless.kabuyoho import Kabuyoho
from src.headless.minkabu import Minkabu
from src.headless.nikkei import Nikkei
from src.headless.reuters import Reuters
from src.headless.toyokeizai import Toyokeizai
from src.headless.yahoo import Yahoo
from src.model.FundamentalData import CompanyProfile


# Kabumap.update_company_profile('6659')
# Nikkei.update_company_profile('6659')
# Kabuyoho.update_company_profile('6659')
# Minkabu.update_company_profile('6659')
# Yahoo.update_company_profile('6659')

Reuters.update_company_profile('6659')

# Toyokeizai.update_company_profile('6659')