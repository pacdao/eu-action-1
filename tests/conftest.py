#!/usr/bin/python3

import pytest
from brownie import Contract, EUMinter, EUWhitelist, VyperNFT


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="function")
def founder_token(minter):
    return Contract(minter.whitelist_tokens(0))


@pytest.fixture(scope="function")
def action_token(minter):
    return Contract(minter.whitelist_tokens(1))


@pytest.fixture(scope="function")
def alice(founder_token, accounts):
    acc = accounts.at(founder_token.ownerOf(1), force=True)
    accounts[9].transfer(acc, accounts[9].balance())
    return acc


@pytest.fixture(scope="function")
def bob(action_token, accounts):
    return accounts.at("0x40E652fE0EC7329DC80282a6dB8f03253046eFde", force=True)


@pytest.fixture(scope="function")
def charlie(accounts):
    return accounts[2]


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="function")
def nft(owner):
    w = EUWhitelist.deploy({"from": owner})
    tokens = [
        "0x63994B223F01b943eFf986b1B379312508dc15F8",  # Founder
        "0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b",  # Gov
        w,
    ]
    nft = VyperNFT.deploy("PAC DAO EU Action NFT 1", "PAC-EU-1", {"from": owner})
    minter = EUMinter.deploy(nft, tokens, {"from": owner})
    nft.transferOwner(minter, {"from": owner})

    return nft


@pytest.fixture(scope="function")
def minter(nft):
    return EUMinter.at(nft.owner())


@pytest.fixture(scope="function")
def minted(minter, alice, bob):
    minter.mint(1, {"from": alice})
    minter.mint(1, {"from": bob})
    return minter


@pytest.fixture(scope="function")
def nft_minted(minted, nft):
    return nft


@pytest.fixture(scope="function")
def nft_funded(minter, accounts):
    accounts[1].transfer(minter, 10 ** 18)
    return minter


@pytest.fixture(scope="function")
def beneficiary(minter, accounts):
    return accounts.at(minter.owner(), force=True)


@pytest.fixture(scope="module")
def gov_addr():
    return "0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b"


@pytest.fixture(scope="function")
def nft_gov(minter, gov_addr):
    minter.set_whitelist_addrs([gov_addr], {"from": minter.owner()})
    return minter


@pytest.fixture(scope="module")
def gov_holder(gov_addr, accounts):
    _addr = "0xbfe384d79969bcb583b8a0e5fedc314aee480e7e"
    return accounts.at(_addr, force=True)


@pytest.fixture(scope="module")
def multi_owner(accounts):
    return accounts.at("0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e", force=True)


# Some NFTs may start at index 1
@pytest.fixture(scope="function")
def initial_id(nft):
    return 0
