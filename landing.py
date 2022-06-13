import streamlit as st 
import pandas 
from plots import *
from utils import *

def landing_page(prices):
    st.markdown("""
                ## stETH/ETH Fluctuation
Analyze the price of stETH in ETH denomination and find meaningful correlations that explain its fluctuation. 
For the task, we'll leverage on seven different tables with Lido's stETH.

1. Daily Staked ETH Balance, Number of Wallets staking, number of unknown wallets, number of known wallets, how much do these wallets own  
(link)[https://app.flipsidecrypto.com/velocity/queries/d00ad07e-6727-4ad6-91ca-b8295fd125ba]  

2. Daily stETH balances via labeled types: CEX, DAPP, DEX, Layer2 etc    
(link)[https://app.flipsidecrypto.com/velocity/queries/1eb4e6a2-533a-4f5b-9c14-78dfe9ef3b5d]  

3. Daily stETH balances via labels: lido, sybil delegate, gate.io, ftx, 1inch, anchor, etc    
(link)[https://app.flipsidecrypto.com/velocity/queries/7cb45579-271d-44e3-adfd-48bf6e755b6a]  

4. Daily stETH balances via labeled subtypes: deposit wallets, treasury, vault, bridge  
(link)[https://app.flipsidecrypto.com/velocity/queries/8f67fdf7-ed11-4156-8433-59ae34c1dbad]    

5. Daily counts and sum from ETH to stETH trades with few pools such as the main curve pool `0xdc24316b9ae028f1497c275eb9192a3ea0f67022` or  uniswap V2-pool.  
(link)[https://app.flipsidecrypto.com/velocity/queries/94f2bb53-3389-47c2-ae39-24840d667d99]   

5. Daily counts and sum from stETH to ETH trades with few pools such as the main curve pool `0xdc24316b9ae028f1497c275eb9192a3ea0f67022` or  uniswap V2-pool.  
(link)[https://app.flipsidecrypto.com/velocity/queries/f52f04e4-8ea3-49c8-91a1-77148da094fd]   

7. stETH and WETH Daily prices.  
(link)[https://app.flipsidecrypto.com/velocity/queries/e28eea67-2919-4bf3-92a6-f002c3db2889]   

Essentially we extract all the data from these queries, and we compute the spearman correlation since the data will not be linear.  
Afterward we visualize the correlation coefficients and show the underlying raw data for each of the variable.  
This is followed by investigating the similarities by clustering a cosine correlation distance matrix for both the dates
and the variables. The purpose is to find some underlying correlation to the stETH-ETH fluctuation. So Voila let's go!
                
If we look at the price data of stETH and wETH we see they are very similar during the past 180 days. However during May the "PEG" started to decline. 
One has to  note that stETH is 1-1 backed with ETH so no real PEG danger exists. Yet the market forces who need fast capital may be tempted to sell their lots via swapping.
                """)
    
    l,r = st.columns(2)
    fig = plot_scatter(prices,'DATE','MEAN_PRICE',c='SYMBOL', text='stETH and WETH vs USD')
    prices_single = prices.query('SYMBOL=="stETH"').merge(prices.query('SYMBOL=="WETH"'),how='left',on='DATE')
    with l:
        st.plotly_chart(fig,use_container_width=True)
    prices_single['MEAN_PRICE'] = prices_single['MEAN_PRICE_x']/prices_single['MEAN_PRICE_y']

    fig = plot_scatter(prices_single,'DATE','MEAN_PRICE',text='stETH vs WETH')
    with r:
        st.plotly_chart(fig,use_container_width=True)
    
    
    st.markdown("""
Let's plot the correlation of each feature, We see that the most negative correlation is the uniswap wallet amounts of stETH to the stETH-ETH peg.
However on inverse, The Uniswap V3's Non Fungible Position Managers wallet sizes are the most positive correlations with the depeg (nf explained)[https://docs.flipsidecrypto.com/our-data/tables/polygon-tables/v3-resources].  
Otherwise it is clear that more the CEX and and DEX have stETH the more depegged it is. Other negatively correlated are the hot wallets, FTX, CEX general label.  
Additionally the bigger the max ETH balances, the less the PEG. All these seem to indicate that the event already happened and the result is high balance wallets or CEX addresses.  
Interestingly most of the addresses with the exception of gate.io and the nf_position_manager tend to negatively correlate with stETH-ETH prices
                """)
    
    
    cors = load_corr()
    st.pyplot(pyplot(cors))
    
    st.markdown("""
Here we can select 1 by one the variable we want investigate against the stETH-ETH peg.  
We see that uniswap balances are near perfect negative correlation with the stETH-ETH peg. 
""")
    
    pair_option = st.selectbox("Select Pair", names,0)
    data = load_pair()
    fig = plot_pair(data, col = pair_option)
    st.pyplot(fig)
    
    st.markdown("""
If we cluster all the variables and the stETH-ETH, we see that in general the stETH is very much negatively correlated with eveything. 
Also, most of the variables tend to correlate with each other which could be clear in the current market conditions.
                """)
    
    fig,groups = clustermap_groups(data,names)
    st.pyplot(fig)
    
    st.markdown("""
If we cluster the dates, we see that the dates cluster nicely to threee different groups based on timestamps. The current group or cluster is the the most different from the previous one
This could indicate bad things or at least breaking from the structures that happened before May.   
                """)
    
    fig,groups = clustermap_dates(data,names)
    st.pyplot(fig)
    
    st.markdown("""
## Conclusion
- The CEX and DEX sizes correlate heavily on the stETH-ETH PEG.
- Also the trading counts punish the stETH-ETH ratio. This indicates that the volume has been depleted and forcing to sell could break the stETH-EHT to new lows.
- Uniswap seems to be the most crucial predictor of changes in the stETH-PEG. We also see that huge amounts have been moved to CEXes when the ratio was low.
                """)