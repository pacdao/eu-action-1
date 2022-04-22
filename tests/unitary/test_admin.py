import brownie
from brownie import ZERO_ADDRESS


def test_new_owner_can_receive(nft_minted, owner, alice, bob):
    nft_minted.updateBeneficiary(bob, {"from": owner})
    bob_init = bob.balance()
    nft_minted.withdraw({"from": alice})
    assert bob.balance() >= bob_init


def test_new_owner_can_withdraw(nft_minted, alice, bob, owner, accounts):
    accounts[0].transfer(nft_minted, 10 ** 18)
    nft_minted.updateBeneficiary(bob, {"from": owner})
    bob_init = bob.balance()
    nft_minted.withdraw({"from": bob})
    assert bob.balance() > bob_init


def test_nonowner_cannot_transfer_owner(nft_minted, alice, bob):
    with brownie.reverts():
        nft_minted.updateBeneficiary(bob, {"from": bob})


def test_new_owner_can_update_owner(nft_minted, alice, bob, owner, accounts):
    nft_minted.updateBeneficiary(bob, {"from": owner})
    nft_minted.updateBeneficiary(alice, {"from": bob})
    accounts[3].transfer(nft_minted, 10 ** 18)
    alice_init = alice.balance()
    nft_minted.withdraw({"from": bob})
    assert alice.balance() > alice_init


def test_fallback_receivable(nft, alice, accounts):
    founder_init = nft.balance()
    accounts[1].transfer(nft, 10 ** 18)
    assert nft.balance() - founder_init == 10 ** 18


def test_fallback_funds_withdrawable(nft, owner, bob, accounts):
    founder_init = nft.balance()
    accounts[0].transfer(nft, 10 ** 18)
    owner_init = owner.balance()
    nft.withdraw({"from": owner})
    assert owner.balance() - owner_init == 10 ** 18 + founder_init


def test_set_token_uri(nft_minted, owner):
    string = "test"
    nft_minted.setTokenUri(1, string, {"from": owner})
    assert nft_minted.tokenURI(1) == nft_minted.baseURI() + string


def test_non_admin_cannot_mint_for(nft, accounts):
    with brownie.reverts("dev: Only Admin"):
        nft.mintFor(accounts[1], {"from": accounts[2]})
    assert nft.balanceOf(accounts[1]) == 0


def test_admin_can_mint_for(nft, accounts, owner):
    assert nft.isWhitelisted(accounts[1]) == False
    nft.mintFor(accounts[1], {"from": owner})
    assert nft.balanceOf(accounts[1]) == 1


def test_non_admin_cannot_set_token_uri(nft_minted, bob):
    init_uri = nft_minted.tokenURI(1)
    string = "test"
    with brownie.reverts("dev: Only Admin"):
        nft_minted.setTokenUri(1, string, {"from": bob})
    assert nft_minted.tokenURI(1) == init_uri


def test_non_admin_cannot_update_token_addrs(nft, bob):
    with brownie.reverts("dev: Only Admin"):
        nft.updateTokenAddrs([ZERO_ADDRESS], {"from": bob})


def test_admin_can_update_token_addrs(nft, owner):
    nft.updateTokenAddrs([ZERO_ADDRESS])
    assert nft.tokenAddrs()[0] == ZERO_ADDRESS
