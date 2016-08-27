#2016/2/18
#cd ../../Google Drive/project/B_finance/fund_invest
#difficulty parsing the website to get the right data such pse, last price, etc.
#see pse_data.py for update
import time
import urllib2
from urllib2 import urlopen

sym = ['I','LOTO','FGEN','MFIN','NOW','SRDC','PERC','FOOD','COL','MPI','AP','NRCP','YEHEY','VLL','PNX','PIP','ALHI','SPH','ORE','EIBB','RWM','ANI','HOUSE','H2O','ALT','NIKL','ROCK','CPM','IMI','EG','MWIDE','DMW','PXP','PGOLD','TECH','EMP','GTCAP','DNL','CAL','COAL','PBB','DMPL','TUGS','AGF','DWC','TFHI','RRHI','CIC','DD','CNPF','TAPET','SSI','PSPC','PGI','X','CROWN','SBS','DATEM','MRSGI','IDC','MER','TEL','EEI','FPH','COSCO','PNB','ICT','HI','PX','KEP','KPH','KPHB','POPI','RLT','MACAY','ANS','ABA','AR','ABS','ACE','MARC','ABG','APO','APX','AT','LR','AB','AC','ALI','PHN','PAL','BPI','BSC','BEL','BC','BCB','BMM','CPV','CPVB','RCI','BCOR','CAT','CEU','CIP','CHIB','CA','CAB','BH','DIZ','ECP','FEU','PAX','FDC','FLI','FYN','FYNB','CYBR','GLO','GPH','IMP','IMPB','MAC','ARA','MCP','IRC','IS','ISM','ATN','ATNB','STI','JGS','JFC','ZHI','GEO','PORT','LC','LFM','PHC','LIHC','MHC','LCB','MBC','MB','MJC','MA','MAB','LTG','SGP','DAVIN','MAH','MAHB','MCB','PMPC','MBT','MED','CPG','OM','OPM','OPMB','JAS','PA','MJIC','V','PCP','IPO','TFC','PBC','PHES','OV','PRC','PTT','PTC','STR','PRIM','PPC','MG','PF','SUN','LRI','REG','WIN','RFM','RCB','RLC','MGH','SMC','SPM','SHNG','WEB','STN','NI','GO','GOB','ACR','TA','FJP','FJPB','UBP','UPM','SGI','EIBA','VUL','SLI','LPZ','SOC','VMC','PCOR','UNI','URC','MEG','SMPH','VVT','PSB','LIB','APC','CEI','CDC','CHI','SFI','AEV','FAF','FNI','SCC','BKR','FPI','VITA','WPI','2GO','GSMI','MRC','PNC','SECB','ION','PLC','LMG','BRN','ELI','LSC','PMT','ATI','DMC','GERI','AAA','HLCM','EVER','UW','ALCO','GREEN','NXGEN','ROX','MVC','BHI','PHA','SLF','BLFI','SM','EDC','SEVN','IPM','EURO','LAND','AUB','AGI','GMA7','MWC','EW','MFC','PSE','BLOOM','BDO','DFNN','CEB','MAXS','CSB','PRMX','T','TBGI','LBC','JOH','SPC']
#sp500 = ['a', 'aa', 'aapl', 'abbv', 'abc', 'abt', 'ace', 'aci', 'acn', 'act', 'adbe', 'adi', 'adm', 'adp', 'adsk', 'adt', 'aee', 'aeo', 'aep', 'aes', 'aet', 'afl', 'agn', 'aig', 'aiv', 'aiz', 'akam', 'all', 'altr', 'alxn', 'amat', 'amd', 'amgn', 'amp', 'amt', 'amzn', 'an', 'anf', 'ann', 'aon', 'apa', 'apc', 'apd', 'aph', 'apol', 'arg', 'arna', 'aro', 'ati', 'atvi', 'avb', 'avp', 'avy', 'axp', 'azo', 'ba', 'bac', 'bax', 'bbby', 'bbry', 'bbt', 'bby', 'bcr', 'bdx', 'beam', 'ben', 'bf-b', 'bhi', 'big', 'biib', 'bk', 'bks', 'blk', 'bll', 'bmc', 'bms', 'bmy', 'brcm', 'brk-b', 'bsx', 'btu', 'bwa', 'bxp', 'c', 'ca', 'cab', 'cag', 'cah', 'cam', 'cat', 'cb', 'cbg', 'cbs', 'cce', 'cci', 'ccl', 'celg', 'cern', 'cf', 'cfn', 'chk', 'chrw', 'ci', 'cim', 'cinf', 'cl', 'clf', 'clx', 'cma', 'cmcsa', 'cme', 'cmg', 'cmi', 'cms', 'cnp', 'cnx', 'cof', 'cog', 'coh', 'col', 'cop', 'cost', 'cov', 'cpb', 'crm', 'csc', 'csco', 'csx', 'ctas', 'ctl', 'ctsh', 'ctxs', 'cvc', 'cvs', 'cvx', 'd', 'dal', 'dd', 'dds', 'de', 'dell', 'df', 'dfs', 'dg', 'dgx', 'dhi', 'dhr', 'dis', 'disca', 'dks', 'dlph', 'dltr', 'dlx', 'dnb', 'dnr', 'do', 'dov', 'dow', 'dps', 'dri', 'dsw', 'dte', 'dtv', 'duk', 'dva', 'dvn', 'ea', 'ebay', 'ecl', 'ed', 'efx', 'eix', 'el', 'emc', 'emn', 'emr', 'eog', 'eqr', 'eqt', 'esrx', 'esv', 'etfc', 'etn', 'etr', 'ew', 'exc', 'expd', 'expe', 'expr', 'f', 'fast', 'fb', 'fcx', 'fdo', 'fdx', 'fe', 'ffiv', 'fhn', 'fis', 'fisv', 'fitb', 'fl', 'flir', 'flr', 'fls', 'flws', 'fmc', 'fosl', 'frx', 'fslr', 'fti', 'ftr', 'gas', 'gci', 'gd', 'ge', 'ges', 'gild', 'gis', 'glw', 'gm', 'gmcr', 'gme', 'gnw', 'goog', 'gpc', 'gps', 'grmn', 'grpn', 'gs', 'gt', 'gww', 'hal', 'har', 'has', 'hban', 'hcbk', 'hcn', 'hcp', 'hd', 'hes', 'hig', 'hog', 'hon', 'hot', 'hov', 'hp', 'hpq', 'hrb', 'hrl', 'hrs', 'hsp', 'hst', 'hsy', 'hum', 'ibm', 'ice', 'iff', 'igt', 'intc', 'intu', 'ip', 'ipg', 'ir', 'irm', 'isrg', 'itw', 'ivz', 'jbl', 'jci', 'jcp', 'jdsu', 'jec', 'jnj', 'jnpr', 'josb', 'joy', 'jpm', 'jwn', 'k', 'key', 'kim', 'klac', 'kmb', 'kmi', 'kmx', 'ko', 'kr', 'krft', 'kss', 'ksu', 'l', 'leg', 'len', 'lh', 'life', 'lll', 'lltc', 'lly', 'lm', 'lmt', 'lnc', 'lo', 'low', 'lrcx', 'lsi', 'ltd', 'luk', 'luv', 'lyb', 'm', 'ma', 'mac', 'mar', 'mas', 'mat', 'mcd', 'mchp', 'mck', 'mco', 'mcp', 'mdlz', 'mdt', 'met', 'mgm', 'mhfi', 'mjn', 'mkc', 'mmc', 'mmm', 'mnst', 'mo', 'molx', 'mon', 'mos', 'mpc', 'mrk', 'mro', 'ms', 'msft', 'msi', 'mtb', 'mu', 'mur', 'mwv', 'myl', 'nbl', 'nbr', 'ndaq', 'ne', 'nee', 'nem', 'nflx', 'nfx', 'ni', 'nile', 'nke', 'nly', 'noc', 'nok', 'nov', 'nrg', 'nsc', 'ntap', 'ntri', 'ntrs', 'nu', 'nue', 'nvda', 'nwl', 'nwsa', 'nyx', 'oi', 'oke', 'omc', 'orcl', 'orly', 'oxy', 'p', 'payx', 'pbct', 'pbi', 'pcar', 'pcg', 'pcl', 'pcln', 'pcp', 'pdco', 'peg', 'pep', 'petm', 'pets', 'pfe', 'pfg', 'pg', 'pgr', 'ph', 'phm', 'pki', 'pld', 'pll', 'pm', 'pnc', 'pnr', 'pnw', 'pom', 'ppg', 'ppl', 'prgo', 'pru', 'psa', 'psx', 'pwr', 'px', 'pxd', 'qcom', 'qep', 'r', 'rai', 'rdc', 'rf', 'rhi', 'rht', 'rl', 'rok', 'rop', 'rost', 'rrc', 'rsg', 'rsh', 'rtn', 's', 'sai', 'sbux', 'scg', 'schl', 'schw', 'sd', 'se', 'see', 'sfly', 'shld', 'shw', 'sial', 'siri', 'sjm', 'sks', 'slb', 'slm', 'sna', 'sndk', 'sne', 'sni', 'so', 'spg', 'spls', 'srcl', 'sre', 'sti', 'stj', 'stt', 'stx', 'stz', 'swk', 'swn', 'swy', 'syk', 'symc', 'syy', 't', 'tap', 'tdc', 'te', 'teg', 'tel', 'ter', 'tgt', 'thc', 'tibx', 'tif', 'tjx', 'tm', 'tmk', 'tmo', 'trip', 'trow', 'trv', 'tsla', 'tsn', 'tso', 'tss', 'twc', 'twx', 'txn', 'txt', 'tyc', 'ua', 'unh', 'unm', 'unp', 'ups', 'urbn', 'usb', 'utx', 'v', 'vale', 'var', 'vfc', 'viab', 'vitc', 'vlo', 'vmc', 'vno', 'vprt', 'vrsn', 'vtr', 'vz', 'wag', 'wat', 'wdc', 'wec', 'wfc', 'wfm', 'whr', 'win', 'wlp', 'wm', 'wmb', 'wmt', 'wpo', 'wpx', 'wtw', 'wu', 'wy', 'wyn', 'wynn', 'x', 'xel', 'xl', 'xlnx', 'xom', 'xray', 'xrx', 'xyl', 'yhoo', 'yum', 'zion', 'zlc', 'zmh', 'znga', 'camp', 'cldx', 'ecyt', 'gtn', 'htz', 'nus', 'pvtb', 'qdel', 'snts', 'wgo', 'wwww']
#sp500short = ['a', 'aa', 'aapl', 'abbv', 'abc', 'abt', 'ace', 'aci', 'acn', 'act', 'adbe', 'adi', 'adm', 'adp']

def yahooKeyStats(stock):
    try:
        #sourceCode = urllib2.urlopen('http://finance.yahoo.com/q/ks?s='+stock).read()
        sourceCode = urllib2.urlopen('http://www.bloomberg.com/quote/'+stock+':PM').read() 
        #pbr = sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
        #pe = sourceCode.split('Current P/E Ratio (TTM) </div> <div class="cell__value cell__value_">')[1].split('</div></div>')[0]
        print sourceCode        
        #print 'price to book ratio:', stock#,pe
        
    except Exception,e:
        print 'failed in the main loop',str(e)

yahooKeyStats(sym[0])
