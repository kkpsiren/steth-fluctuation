import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page
from beautify import flipside_logo, discord_logo
import os

from utils import *    

st.set_page_config(page_title="Flipside Crypto:Lido stETH vs ETH Depeg", layout="wide")

prices = load_prices()

st.sidebar.markdown("#### Connect")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()
flipside_logo(url="https://godmode.flipsidecrypto.xyz/")
landing_page(prices)
