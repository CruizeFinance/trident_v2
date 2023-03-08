import json

from components import FirebaseDataManager
from services import api_services
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

    def get_contract(self):
        contracts_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        # Testing Data
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
        contract = self.get_contract()
        assets = contract[network_name]
        asset_tvl = self.get_asset_tvl(
            assets[asset_symbol],
            constant.symbol_asset[asset_symbol],
            constant.asset_decimals[asset_symbol],
            contract[network_name]["contract_obj"],
            network_name,
            asset_symbol,
        )
        return asset_tvl

    def network_total_tvl(self, network_id):
        network_name = constant.networks[network_id]
        assets_total_tvl = {}
        contracts = self.get_contract()
        contract_obj = contracts[network_name]["contract_obj"]
        assets = contracts[network_name]

        for asset_symbol, asset_address in assets.items():
            if asset_symbol not in constant.symbol_asset.keys():
                continue
            asset_tvl = self.get_asset_tvl(
                asset_address=asset_address,
                asset_name=constant.symbol_asset[asset_symbol],
                decimals=constant.asset_decimals[asset_symbol],
                contract=contract_obj,
                network_name=network_name,
                asset_symbol=asset_symbol,
            )["tvl"]
            assets_total_tvl[asset_symbol] = asset_tvl
        return assets_total_tvl

    def total_tvl(self, network_env):
        total_tvl = {}
        network_names = constant.networks[network_env].values()
        contracts = self.get_contract()

        for i, network_name in enumerate(network_names):
            total_tvl[network_name] = {}
            network_data = contracts.get(network_name, None)
            if not network_data:
                continue

            contract_obj = network_data["contract_obj"]
            assets = contracts[network_name]
            for asset_symbol, asset_address in assets.items():
                if asset_symbol not in constant.symbol_asset.keys():
                    continue
                asset_tvl = self.get_asset_tvl(
                    asset_address=asset_address,
                    asset_name=constant.symbol_asset[asset_symbol],
                    decimals=constant.asset_decimals[asset_symbol],
                    contract=contract_obj,
                    network_name=network_name,
                    asset_symbol=asset_symbol,
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
        self, asset_address, asset_name, decimals, contract, network_name, asset_symbol
    ):
        asset_address = Web3.toChecksumAddress(asset_address)
        asset_tvl_info = contract.functions.vaults(asset_address).call()
        asset_cap = asset_tvl_info[4] / constant.asset_decimals[asset_symbol]
        asset_tvl = asset_tvl_info[1] + asset_tvl_info[2]
        asset_tvl = asset_tvl / decimals
        if network_name == "goerli":
            asset_tvl = asset_tvl + constant.asset_tvl[asset_name]
        asset_info = {"vault_cap": asset_cap, "tvl": asset_tvl}
        return asset_info


if __name__ == "__main__":
    a = CruizeContract()
    # print(a.asset_tvl("USDC", "5"))
    # print(a.total_tvl())
    # print(a.network_total_tvl('5'))
