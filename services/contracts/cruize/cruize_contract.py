from components import FirebaseDataManager
from services import api_services
from services.contracts import LoadContracts
from utilities import constant


class CruizeContract(object):
    def __init__(self):
        self.load_contract = LoadContracts()
        contract_abi = open("cruize_contract_abi.json")

        self.firebase_db_manager_obj = FirebaseDataManager()
        cruize_contract = self.firebase_db_manager_obj.fetch_data("contracts", "cruize_contract")
        self.contract = self.load_contract.load_contracts(
            cruize_contract["address"][0], contract_abi
        )
        self.w3 = self.load_contract.web3_provider()

    def asset_tvl(self, asset_symbol):
        asset_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        assets = asset_data["address"]
        asset_tvl = self.get_asset_tvl(
            assets[asset_symbol],
            constant.symbol_asset[asset_symbol],
            constant.asset_decimals[asset_symbol],
        )
        return asset_tvl

    def all_assets_tvl(self):
        asset_data = self.firebase_db_manager_obj.fetch_data("contracts", "cruize")
        assets = asset_data["address"]
        assets_total_tvl = {}
        for asset_symbol, asset_address in assets.items():
            asset_tvl = self.get_asset_tvl(
                asset_address,
                constant.symbol_asset[asset_symbol],
                constant.asset_decimals[asset_symbol],
            )["tvl"]
            assets_total_tvl[asset_symbol] = asset_tvl
        return assets_total_tvl

    def get_asset_tvl(self, asset_address, asset_name, decimals):
        asset_tvl_info = self.contract.functions.vaults(asset_address).call()

        asset_cap = asset_tvl_info[4] / constant.asset_cap_decimal
        asset_tvl = asset_tvl_info[1] + asset_tvl_info[2]
        asset_tvl = asset_tvl / decimals
        asset_tvl = asset_tvl + constant.asset_tvl[asset_name]

        asset_info = {"vault_cap": asset_cap, "tvl": asset_tvl}
        return asset_info


if __name__ == "__main__":
    a = CruizeContract()
    print(
        a.get_asset_tvl("0xf4423F4152966eBb106261740da907662A3569C5", "bitcoin", 1e18)
    )
