import brownie
from brownie import Wei, history


def test_alice_can_mint(nft, minter, initial_id, alice):
    minter.mint(1, {"from": alice, "value": minter.mint_price()})
    assert nft.ownerOf(initial_id) == alice


def test_alice_second_mint_costs(minted, alice):
    with brownie.reverts():
        minted.mint(1, {"from": alice, "value": 0})


def test_alice_can_pay_for_seconds(nft, minted, initial_id, alice):
    minted.mint(1, {"from": alice, "value": minted.mint_price()})
    assert nft.ownerOf(initial_id) == alice


def test_nonowner_cannot_mint_for_free(minted, accounts):
    assert minted.is_whitelisted(accounts[3]) == False
    with brownie.reverts():
        minted.mint(1, {"from": accounts[3]})


def test_has_minted_starts_false(minter, alice):
    assert minter.has_minted(alice) == False


def test_has_minted_updates(minted, alice):
    assert minted.has_minted(alice) == True


def test_id_updates_on_mint(nft, minter, initial_id, bob):
    minter.mint(1, {"from": bob, "value": minter.mint_price()})
    assert nft.balanceOf(bob) > 0
    assert nft.totalSupply() == nft.balanceOf(bob)


def test_assert_token_received(nft, minted, initial_id, bob):
    assert nft.ownerOf(nft.totalSupply() - 1 + initial_id) == bob


def test_mint_price_reasonable(minter, alice):
    minter.mint(1, {"from": alice})
    assert history[-1].gas_used * Wei("50 gwei") / 10 ** 18 < 0.01


def test_mint_many_receives_many(minter, nft, multi_owner):
    minter.mint(
        5,
        {"from": multi_owner, "value": minter.user_price_for_quantity(5, multi_owner)},
    )
    assert nft.balanceOf(multi_owner) == 5


def test_cannot_mint_after_mint_deactivated(minter, multi_owner):
    minter.set_is_active(False)
    with brownie.reverts():
        minter.mint(
            1,
            {
                "from": multi_owner,
                "value": minter.user_price_for_quantity(1, multi_owner),
            },
        )
