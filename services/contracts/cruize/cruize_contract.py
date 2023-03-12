import json

from components import FirebaseDataManager
from services.contracts import LoadContracts
from utilities import constant

from web3 import Web3


class CruizeContract(object):
    def __init__(self):
        self.load_contract = LoadContracts()
        # self.contract_abi = open(
        #     "/home/CruizeFinance/trident_v2/services/contracts/cruize/cruize_contract_abi.json"
        # )
        self.contract_abi = open("services/contracts/cruize/cruize_contract_abi.json")
        self.contract_data = json.load(self.contract_abi)
        self.firebase_db_manager_obj = FirebaseDataManager()

    def get_contract(self, network_names):
        contracts_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        # TODO: Testing Data -- Don't remove
        # contracts_data = {
        #     "arbitrum-goerli": {
        #         "address": "0x7554f9068b4169C9B2fC4C4488A5509201045665",
        #         "WBTC": "0x295476C268e13f14967518D58E384d46b190b196",
        #         "USDC": "0x9c4994967C29E807b75dbf85fF69261F47362817",
        #         "WETH": "0xB1BdbaA3A41df99701c5de37Ca6e42E87227fd54",
        #     },
        #     "goerli": {
        #         "address": "0x23800A9DB5dE3c8e0d33E858461d33181298f2D0",
        #         "WETH": "0xB8096bC53c3cE4c11Ebb0069Da0341d75264B104",
        #         "WBTC": "0x02245d57122896af490174f7421bD5a73CF7b0dc",
        #         "USDC": "0xf029E7204D23A97CCd788e808c0f45ddB6745b25",
        #     },
        #     "polygon-mumbai": {
        #         "WETH": "0xafAa83252d90B6a209000eC389E943b03FdCB0F8",
        #         "WBTC": "0xedC7632768B7239BBA9F66cB807e14Cb7aF7a04E",
        #         "address": "0x08d3B3dF4512F7C437Bb149fA7b10FF7cA9A6c5E",
        #         "USDC": "0xE7AFdD06DfD32a3175687D77Fd9a4eD270d7E814",
        #     },
        # }

        for network_name, network_data in contracts_data.items():
            address = network_data["address"]
            if network_name in network_names:
                print("network_name: ", network_name)
                contract = self.load_contract.load_contracts(
                    address, self.contract_data, network_name
                )
                contracts_data[network_name]["contract_obj"] = contract
        return contracts_data

    def asset_tvl(self, asset_symbol, network_id):
        networks = constant.networks.values()
        network_name = ""
        for network in networks:
            if network_id in network.keys():
                network_name = network[network_id]

        contract = self.get_contract([network_name])
        assets = contract[network_name]["assets"]
        asset_tvl = self.get_asset_tvl(
            assets[asset_symbol],
            asset_symbol,
            contract[network_name]["contract_obj"],
        )
        return asset_tvl

    # TODO : Add function to get a networks total TVL
    # def network_total_tvl(self, network_id):
    #     network_name = constant.networks[network_id]
    #     assets_total_tvl = {}
    #     contracts = self.get_contract([network_name])
    #     contract_obj = contracts[network_name]["contract_obj"]
    #     assets = contracts[network_name]
    #
    #     for asset_symbol, asset_address in assets.items():
    #         if asset_symbol not in constant.symbol_asset.keys():
    #             continue
    #         asset_tvl = self.get_asset_tvl(
    #             asset_address=asset_address,
    #             asset_name=constant.symbol_asset[asset_symbol],
    #             decimals=constant.asset_decimals[asset_symbol],
    #             contract=contract_obj,
    #             network_name=network_name,
    #             asset_symbol=asset_symbol,
    #         )["tvl"]
    #         assets_total_tvl[asset_symbol] = asset_tvl
    #     return assets_total_tvl

    def total_tvl(self, network_env):
        total_tvl = {}
        network_names = constant.networks[network_env].values()
        contracts = self.get_contract(network_names)

        for i, network_name in enumerate(network_names):
            total_tvl[network_name] = {}
            network_data = contracts.get(network_name, None)
            if not network_data:
                continue

            if network_name not in network_names:
                continue

            contract_obj = network_data["contract_obj"]
            asset_addresses = list(contracts[network_name]["assets"].values())
            asset_symbols = list(contracts[network_name]["assets"].keys())

            network_asset_data = self.get_tokens_tvl(
                asset_addresses,
                asset_symbols,
                contract_obj,
                network_name,
            )

            total_tvl[network_name] = network_asset_data[network_name]

        tvl = {}
        for network, network_asset_data in total_tvl.items():
            for asset_symbol, asset_tvl in network_asset_data["tvl"].items():
                if asset_symbol not in tvl:
                    tvl[asset_symbol] = 0
                tvl[asset_symbol] += asset_tvl
        return tvl

    def get_tokens_tvl(
        self,
        asset_addresses,
        asset_symbols,
        contract,
        network_name,
    ):
        asset_checksum_address = []
        for asset_address in asset_addresses:
            print(asset_address)
            asset_checksum_address.append(Web3.toChecksumAddress(asset_address))

        tokens_tvl = contract.functions.tokensTvl(asset_checksum_address).call()

        asset_tvl_data = {network_name: {"vault_cap": {}, "tvl": {}}}
        for i, asset_symbol in enumerate(asset_symbols):
            asset_cap = tokens_tvl[i][1] / constant.asset_decimals[asset_symbol]
            asset_tvl = tokens_tvl[i][0] / constant.asset_decimals[asset_symbol]
            asset_tvl_data[network_name]["vault_cap"][asset_symbol] = asset_cap
            asset_tvl_data[network_name]["tvl"][asset_symbol] = asset_tvl

        return asset_tvl_data

    def get_asset_tvl(
        self,
        asset_address,
        asset_symbol,
        contract,
    ):
        asset_address = Web3.toChecksumAddress(asset_address)
        decimals = constant.asset_decimals[asset_symbol]
        asset_tvl_info = contract.functions.tokensTvl([asset_address]).call()
        asset_cap = asset_tvl_info[0][1] / decimals
        asset_tvl = asset_tvl_info[0][0] / decimals
        asset_info = {"vault_cap": asset_cap, "tvl": asset_tvl}
        return asset_info


if __name__ == "__main__":
    a = CruizeContract()
    print(a.asset_tvl("USDC", "421613"))
    # print(a.total_tvl("testnet"))
    # print(a.network_total_tvl('5'))
