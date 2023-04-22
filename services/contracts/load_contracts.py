import json
from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware

# class -  LoadContracts: is responsible for lading contract and web3
from utilities import constant


class LoadContracts:

    """
    :method - load_contracts.
    :params - contract_address: address of contract to load.
    :params - contract_abi: abi of contract to load.
    :return - contract instance.
    """

    def load_contracts(self, contract_address, contract_abi, network_name):
        w3 = self.web3_provider(network_name)
        contract_address = w3.toChecksumAddress(contract_address)
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        return contract

    """
      :method -  web3_provider:load web3 provider.
      :return - web3 instance. 
    """

    def web3_provider(self, network_name):
        print("calling web3 provider")
        infura = "790e7e620ecc47b5bf249d1e936b3cca"
        if network_name not in constant.networks["mainnet"].values():
            # infura_testnet = config("INFURA_TESTNET")

            web3 = Web3(
                Web3.HTTPProvider(f"https://{network_name}.infura.io/v3/{infura}")
            )
        else:
            # infura_mainnet = config("INFURA_MAINNET")
            web3 = Web3(
                Web3.HTTPProvider(
                    f"https://{network_name}-mainnet.infura.io/v3/{infura}"
                )
            )
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3
