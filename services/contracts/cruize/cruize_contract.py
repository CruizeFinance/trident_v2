from components import FirebaseDataManager
from services import api_services
from services.contracts import LoadContracts
from utilities import constant


class CruizeVault:
    def __init__(self):
        self.load_contract = LoadContracts()
        contract_abi = open("/home/CruizeFinance/trident_v2/services/contracts/cruize/cruize_contract_abi.json")
        self.firebase_db_manager_obj = FirebaseDataManager()
        self.contract = self.load_contract.load_contracts(
            constant.CRUIZE_CONTRACT, contract_abi
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
            )
            assets_total_tvl [asset_symbol] = asset_tvl
        return assets_total_tvl

    def get_asset_tvl(self, asset_address, asset_name, decimals):
        asset_tvl_info = self.contract.functions.vaults(asset_address).call()
        asset_tvl = asset_tvl_info[1] + asset_tvl_info[2]
        asset_tvl = asset_tvl / decimals
        asset_tvl = asset_tvl + constant.asset_tvl[asset_name]
        return asset_tvl


if __name__ == "__main__":
    a = CruizeVault()
