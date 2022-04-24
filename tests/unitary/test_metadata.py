import brownie
import pytest


def test_token_uri_ipfs(nft_minted):
    assert nft_minted.tokenURI(1)[0:7] == "ipfs://"


def test_mints_with_updated_metadata(nft, minter, owner, alice):
    new_data = "new_uri"
    minter.set_default_metadata(new_data, {"from": owner})
    minter.mint(1, {"from": alice})

    assert nft.tokenURI(nft.totalSupply()) == nft.baseURI() + new_data


def test_new_owner_can_update_metadata(nft, minter, alice, bob, owner):
    minter.set_owner(bob, {"from": owner})
    new_data = "new uri"
    minter.set_default_metadata(new_data, {"from": bob})
    minter.mint(1, {"from": alice})
    assert nft.tokenURI(nft.totalSupply()) == nft.baseURI() + new_data


@pytest.mark.skip()
def test_contract_uri(nft):
    assert nft.contractURI() == "ipfs://QmXqtMKHL5AKQE8VhumF9aH5MeyPuwvd7m9KS5d22GKdhm"


def test_nonadmin_cannot_update_contract_uri(nft, accounts):
    with brownie.reverts():
        nft.setContractURI("test", {"from": accounts[2]})


def test_contract_uri_updates(nft, minter, owner):
    minter.set_contract_uri("test", {"from": owner})
    assert nft.contractURI() == "ipfs://test"
