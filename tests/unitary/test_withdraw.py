def test_can_withdraw_as_alice(nft_funded, alice, bob, accounts, beneficiary):
    nft_funded.withdraw({"from": alice})
    init_balance = beneficiary.balance()
    accounts[1].transfer(nft_funded, 10 ** 18)
    nft_funded.mint(1, {"from": bob})
    nft_funded.withdraw({"from": alice})
    final_balance = beneficiary.balance()
    assert final_balance - init_balance == 10 ** 18


def test_can_withdraw_as_bob(nft_funded, alice, bob, accounts, beneficiary):
    nft_funded.withdraw({"from": alice})
    init_balance = beneficiary.balance()

    accounts[1].transfer(nft_funded, 10 ** 18)
    nft_funded.mint(1, {"from": bob})
    nft_funded.withdraw({"from": bob})
    final_balance = beneficiary.balance()
    assert final_balance - init_balance == 10 ** 18


def test_bob_gets_nothing_on_withdraw(nft_funded, bob):
    bob_balance = bob.balance()
    nft_funded.withdraw({"from": bob})
    assert bob.balance() <= bob_balance


def test_withdrawal_increases_balance(nft_funded, alice, accounts, beneficiary):
    init_balance = beneficiary.balance()
    accounts[3].transfer(nft_funded, 10 ** 18)
    nft_funded.withdraw({"from": alice})
    final_balance = beneficiary.balance()
    assert final_balance > init_balance


def test_can_receive_funds_through_fallback(nft, alice, bob, accounts, beneficiary):
    init_balance = beneficiary.balance()
    bob_balance = bob.balance()
    accounts[3].transfer(nft, 10 ** 18)

    bob.transfer(nft, bob_balance)
    nft.withdraw({"from": alice})
    final_balance = beneficiary.balance()
    assert final_balance - init_balance >= bob_balance
