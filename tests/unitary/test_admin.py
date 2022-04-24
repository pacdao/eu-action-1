import brownie
from brownie import ZERO_ADDRESS


def test_new_owner_can_receive(minted, owner, alice, bob):
    minted.set_owner(bob, {"from": owner})
    bob_init = bob.balance()
    minted.withdraw({"from": alice})
    assert bob.balance() >= bob_init


def test_new_owner_can_withdraw(minted, alice, bob, owner, accounts):
    accounts[0].transfer(minted, 10 ** 18)
    minted.set_owner(bob, {"from": owner})
    bob_init = bob.balance()
    minted.withdraw({"from": bob})
    assert bob.balance() > bob_init


def test_nonowner_cannot_transfer_owner(minted, alice, bob):
    with brownie.reverts():
        minted.set_owner(bob, {"from": bob})


def test_new_owner_can_update_owner(minted, alice, bob, owner, accounts):
    minted.set_owner(bob, {"from": owner})
    minted.set_owner(alice, {"from": bob})
    accounts[3].transfer(minted, 10 ** 18)
    alice_init = alice.balance()
    minted.withdraw({"from": bob})
    assert alice.balance() > alice_init


def test_fallback_receivable(minter, alice, accounts):
    founder_init = minter.balance()
    accounts[1].transfer(minter, 10 ** 18)
    assert minter.balance() - founder_init == 10 ** 18


def test_fallback_funds_withdrawable(minter, owner, bob, accounts):
    founder_init = minter.balance()
    accounts[0].transfer(minter, 10 ** 18)
    owner_init = owner.balance()
    minter.withdraw({"from": owner})
    assert owner.balance() - owner_init == 10 ** 18 + founder_init


def test_set_token_uri(minted, nft, owner):
    string = "test"
    minted.set_token_uri(1, string, {"from": owner})

    assert nft.tokenURI(1) == string


def test_non_admin_cannot_mint_for(minter, nft, accounts):
    with brownie.reverts():
        minter.mint_for(accounts[1], {"from": accounts[2]})
    assert nft.balanceOf(accounts[1]) == 0


def test_admin_can_mint_for(minter, nft, accounts, owner):
    assert minter.is_whitelisted(accounts[1]) == False
    minter.mint_for(accounts[1], {"from": owner})
    assert nft.balanceOf(accounts[1]) == 1


def test_non_admin_cannot_set_token_uri(minted, nft, bob):
    init_uri = nft.tokenURI(1)
    string = "test"
    with brownie.reverts():
        minted.set_token_uri(1, string, {"from": bob})
    assert nft.tokenURI(1) == init_uri


def test_non_admin_cannot_update_token_addrs(minted, bob):
    with brownie.reverts():
        minted.set_whitelist_addrs([ZERO_ADDRESS], {"from": bob})


def test_admin_can_update_token_addrs(minted, owner):
    assert minted.whitelist_tokens(0) != ZERO_ADDRESS
    minted.set_whitelist_addrs([ZERO_ADDRESS])
    assert minted.whitelist_tokens(0) == ZERO_ADDRESS
