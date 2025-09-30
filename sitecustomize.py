import warnings
from urllib3.exceptions import NotOpenSSLWarning

# Suprimir permanentemente o NotOpenSSLWarning de urllib3
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)