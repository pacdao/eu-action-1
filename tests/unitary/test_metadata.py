import brownie


def test_token_uri_ipfs(nft_minted):
    assert nft_minted.tokenURI(1)[0:7] == "ipfs://"


def test_mints_with_updated_metadata(nft, owner, alice):
    new_data = "new_uri"
    nft.setDefaultMetadata(new_data, {"from": owner})
    nft.mint(1, {"from": alice})
    assert nft.tokenURI(nft.totalSupply()) == nft.baseURI() + new_data


def test_new_owner_can_update_metadata(nft, alice, bob, owner):
    founder = nft
    founder.updateBeneficiary(bob, {"from": owner})
    new_data = "new uri"
    founder.setDefaultMetadata(new_data, {"from": bob})
    founder.mint(1, {"from": alice})
    assert founder.tokenURI(founder.totalSupply()) == founder.baseURI() + new_data


def test_contract_uri(nft):
    assert nft.contractURI() == "ipfs://QmXqtMKHL5AKQE8VhumF9aH5MeyPuwvd7m9KS5d22GKdhm"


def test_nonadmin_cannot_update_contract_uri(nft, accounts):
    with brownie.reverts("dev: Only Admin"):
        nft.setContractURI("test", {"from": accounts[2]})


def test_contract_uri_updates(nft, owner):
    nft.setContractURI("test", {"from": owner})
    assert nft.contractURI() == "ipfs://test"
