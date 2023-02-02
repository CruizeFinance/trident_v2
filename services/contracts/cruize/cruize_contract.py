import json

from components import FirebaseDataManager
from services import api_services
from services.contracts import LoadContracts
from utilities import constant
from joblib import Parallel, delayed

from web3 import Web3


class CruizeContract(object):
    def __init__(self):
        self.load_contract = LoadContracts()
        self.contract_abi = open(
            "/home/CruizeFinance/trident_v2/services/contracts/cruize/cruize_contract_abi.json"
        )
        # self.contract_abi = open("/Users/prithvirajmurthy/Desktop/blockchain/cruize/trident_v2/services/contracts/cruize/cruize_contract_abi.json")
        self.contract_data = json.load(self.contract_abi)
        self.firebase_db_manager_obj = FirebaseDataManager()

    def get_contract(self, network):
        cruize_contract = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        contract = self.load_contract.load_contracts(
            cruize_contract[network + "_address"], self.contract_data, network
        )
        return contract

    def asset_tvl(self, asset_symbol, network_id):
        #  network name from network id
        network_name = constant.network_name[network_id]
        contract = self.get_contract(network_name)
        asset_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        assets = asset_data[network_name]
        asset_tvl = self.get_asset_tvl(
            assets[asset_symbol],
            constant.symbol_asset[asset_symbol],
            constant.asset_decimals[asset_symbol],
            contract,
            network_name,
        )
        return asset_tvl

    def network_total_tvl(self, network_id):
        network_name = constant.network_name[network_id]
        contract = self.get_contract(network_name)
        asset_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        assets = asset_data[network_name]
        assets_total_tvl = {}
        for asset_symbol, asset_address in assets.items():
            asset_tvl = self.get_asset_tvl(
                asset_address,
                constant.symbol_asset[asset_symbol],
                constant.asset_decimals[asset_symbol],
                contract,
                network_name,
            )["tvl"]
            assets_total_tvl[asset_symbol] = asset_tvl
        return assets_total_tvl

    def total_tvl(self):
        total_tvl = {}
        network_names = constant.network_name.values()

        for network_name in network_names:
            total_tvl[network_name] = {}
            contract = self.get_contract(network_name)
            asset_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
            assets = asset_data[network_name]
            for asset_symbol, asset_address in assets.items():
                asset_tvl = self.get_asset_tvl(
                    asset_address,
                    constant.symbol_asset[asset_symbol],
                    constant.asset_decimals[asset_symbol],
                    contract,
                    network_name,
                )["tvl"]
                total_tvl[network_name][asset_symbol] = asset_tvl

        # total_tvl = {"goerli": {"wbtc": 212, "weth": 2344}, "shardeum": {"wbtc": 2, "weth": 244} }
        tvl = {}
        for network, network_tvl in total_tvl.items():
            for asset, asset_tvl in network_tvl.items():
                if asset not in tvl:
                    tvl[asset] = 0
                tvl[asset] += asset_tvl
        return tvl

    def get_asset_tvl(
        self, asset_address, asset_name, decimals, contract, network_name
    ):
        asset_address = Web3.toChecksumAddress(asset_address)
        asset_tvl_info = contract.functions.vaults(asset_address).call()

        asset_cap = asset_tvl_info[4] / constant.asset_cap_decimal
        asset_tvl = asset_tvl_info[1] + asset_tvl_info[2]
        asset_tvl = asset_tvl / decimals
        if network_name == "goerli":
            asset_tvl = asset_tvl + constant.asset_tvl[asset_name]
        asset_info = {"vault_cap": asset_cap, "tvl": asset_tvl}
        return asset_info


if __name__ == "__main__":
    a = CruizeContract()
    # print(a.total_tvl())
    print(a.asset_tvl("WBTC", "5"))
