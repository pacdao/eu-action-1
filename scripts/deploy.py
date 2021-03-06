from brownie import ZERO_ADDRESS, accounts, network, EUWhitelist, VyperNFT, EUMinter
from brownie.network import max_fee, priority_fee


def main():
    publish_source = True
    multisig = "0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e"
    beneficiary_address = multisig

    if network.show_active() in ["development"]:
        tokens = [ZERO_ADDRESS]
        deployer = accounts[0]
        publish_source = False
        beneficiary_address = deployer

    elif network.show_active() in ["rinkeby", "ropsten"]:
        if network.show_active() == "rinkeby":
            tokens = [
                # "0x63994B223F01b943eFf986b1B379312508dc15F8",  # Founder
                # "0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b",  # Gov
            ]
        else:
            tokens = []

        deployer = accounts.load("husky")
        beneficiary_address = deployer
        publish_source = False
    elif network.show_active() in ["mainnet", "mainnet-fork"]:
        tokens = [
            "0x63994B223F01b943eFf986b1B379312508dc15F8",  # Founder
            "0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b",  # Gov
        ]

        if network.show_active() == "mainnet-fork":
            publish_source = False
            deployer = accounts[0]
        if network.show_active() == "mainnet":
            deployer = accounts.load("minnow")
            max_fee(input("Max fee in gwei: ") + " gwei")
            priority_fee("2 gwei")
            publish_source = True
    else:
        deployer = accounts.load("husky")
        publish_source = True

    w = EUWhitelist.deploy({"from": deployer})
    tokens.append(w)

    nft = VyperNFT.deploy("PAC DAO EU Action NFT 1", "PAC-EU-1", {'from': deployer}, publish_source=publish_source)
    minter = EUMinter.deploy(nft, tokens, {'from': deployer}, publish_source=publish_source)
    nft.transferMinter(minter, {'from': deployer})
    return minter

