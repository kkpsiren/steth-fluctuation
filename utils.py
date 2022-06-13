import pandas as pd

def load_prices():
    prices = pd.read_csv('data/steth-price-daily.csv')
    prices['DATE'] = pd.to_datetime(prices['DATE'])
    return prices

def load_corr():
    df = pd.read_csv('data/correlations.csv')
    return df

def load_pair():
    prices = pd.read_csv('data/steth-price-daily.csv')
    prices['DATE'] = pd.to_datetime(prices['DATE'])
    prices_single = prices.query('SYMBOL=="stETH"').merge(prices.query('SYMBOL=="WETH"'),how='left',on='DATE')
    prices_single['MEAN_PRICE'] = prices_single['MEAN_PRICE_x']/prices_single['MEAN_PRICE_y']
    data = prices_single[['DATE','MEAN_PRICE']]
    data.index=data['DATE']
    d1 = pd.read_csv('data/lido-staked-label-subtypes.csv').pivot_table(index='BALANCE_DATE',columns='LABEL_SUBTYPE',values='STAKED_ETH_BALANCE')
    d1.index = pd.to_datetime(d1.index)
    d2 = pd.read_csv('data/lido-staked-labels.csv').pivot_table(index='BALANCE_DATE',columns='LABEL',values='STAKED_ETH_BALANCE')
    d2.index = pd.to_datetime(d2.index)
    d3 = pd.read_csv('data/lido-label-type.csv').pivot_table(index='BALANCE_DATE',columns='LABEL_TYPE',values='STAKED_ETH_BALANCE')
    d3.index = pd.to_datetime(d3.index)
    d4 = pd.read_csv('data/balances.csv',index_col=0)
    d4.index = pd.to_datetime(d4.index)
    d5 = pd.read_csv('data/lido-eth-steth.csv',index_col=0)
    d5.index = pd.to_datetime(d5.index)
    d6=d5.resample('1d')['GAIN_OR_LOSS'].agg(['count','sum'])
    d7=d5.groupby('POOL_NAME').resample('1d')['GAIN_OR_LOSS'].agg(['count','sum']).reset_index().pivot_table(index='DATE',columns='POOL_NAME',values='count')
    d5=d5.groupby('POOL_NAME').resample('1d')['GAIN_OR_LOSS'].agg(['count','sum']).reset_index().pivot_table(index='DATE',columns='POOL_NAME',values='sum')
    d7.columns = [f'{i}-eth-steth-count' for i in d7.columns]
    d6.columns = [f'{i}-eth-steth-count' for i in d6.columns]
    d5.columns = [f'{i}-eth-steth-sum' for i in d5.columns]
    d8 = pd.read_csv('data/lido-steth-eth.csv',index_col=0)
    d8.index = pd.to_datetime(d8.index)
    d9=d8.resample('1d')['GAIN_OR_LOSS'].agg(['count','sum'])
    d10=d8.groupby('POOL_NAME').resample('1d')['GAIN_OR_LOSS'].agg(['count','sum']).reset_index().pivot_table(index='DATE',columns='POOL_NAME',values='count')
    d8=d8.groupby('POOL_NAME').resample('1d')['GAIN_OR_LOSS'].agg(['count','sum']).reset_index().pivot_table(index='DATE',columns='POOL_NAME',values='sum')
    d10.columns = [f'{i}-steth-eth-count' for i in d10.columns]
    d9.columns = [f'{i}-steth-eth-count' for i in d10.columns]
    d8.columns = [f'{i}-steth-eth-sum' for i in d8.columns]
    data = data.join(d1.join(d2).join(d3).join(d4).join(d5).join(d6).join(d7).join(d8).join(d9).join(d10))
    return data

names = ['uniswap',
 'hot_wallet',
 'cex',
 'ftx',
 'inverse finance',
 'contract_deployer',
 'opportunist',
 'MAX_ETH_BALANCE',
 '0xdc24316b9ae028f1497c275eb9192a3ea0f67022-steth-eth-count',
 'stETH-WETH LP-eth-steth-count',
 'general_contract',
 'stETH-WETH LP-steth-eth-count',
 'ribbon finance',
 'swap_contract',
 'NUMBER_WALLETS',
 'NON_LABELED_WALLET_COUNTS',
 'LABELED_WALLET_COUNTS',
 'STAKED_ETH_BALANCE',
 'treasury',
 'deposit_wallet',
 'NON_LABELED_WALLET_SUM',
 'token_contract',
 'lido',
 'AVERAGE_ETH_BALANCE',
 'layer2',
 'toxic',
 '0xdc24316b9ae028f1497c275eb9192a3ea0f67022-eth-steth-count',
 'dapp',
 'dex',
 'curve fi',
 'pool',
 '1inch',
 'LABELED_WALLET_SUM',
 'distributor_cex',
 'defi',
 'sybil delegate',
 'vault',
 'anchor',
 'gate.io',
 'nf_position_manager']
