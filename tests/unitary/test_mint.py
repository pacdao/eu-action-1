import brownie
from brownie import Wei, history


def test_alice_can_mint(nft, alice):
    nft.mint(1, {"from": alice})
    assert nft.ownerOf(1) == alice


def test_alice_second_mint_costs(nft_minted, alice):
    with brownie.reverts("dev: Insufficient Funds"):
        nft_minted.mint(1, {"from": alice})


def test_alice_can_pay_for_seconds(nft_minted, alice):
    nft_minted.mint(1, {"from": alice, 'value': nft_minted.mintPrice()})
    assert nft_minted.ownerOf(nft_minted.totalSupply()) == alice


def test_nonowner_cannot_mint_for_free(nft_minted, accounts):
    with brownie.reverts("dev: Insufficient Funds"):
        nft_minted.mint(1, {"from": accounts[3]})


def test_has_minted_starts_false(nft, alice):
    assert nft.hasMinted(alice) == False


def test_has_minted_updates(nft_minted, alice):
    assert nft_minted.hasMinted(alice) == True


def test_id_updates_on_mint(nft, bob):
    founder = nft
    first_id = founder.currentId()
    founder.mint(1, {"from": bob})
    assert founder.balanceOf(bob) > 0
    assert founder.currentId() == first_id + founder.balanceOf(bob)


def test_assert_token_received(nft_minted, bob):
    founder = nft_minted
    curr_id = founder.currentId()
    assert founder.ownerOf(curr_id ) == bob


def test_mint_price_reasonable(nft, alice):
    nft.mint(1, {"from": alice})
    assert history[-1].gas_used * Wei("50 gwei") / 10 ** 18 < (
        0.02 * nft.balanceOf(alice)
    )


def test_mint_many_receives_many(nft, multi_owner):
    nft.mint(2, {"from": multi_owner, 'value': nft.userPriceForQuantity(2, multi_owner)})
    assert nft.balanceOf(multi_owner) == 2
