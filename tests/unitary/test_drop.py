from brownie import ZERO_ADDRESS, PACDaoEUAction


def test_non_beneficiary_can_deploy(alice, bob):
    PACDaoEUAction.deploy(alice, [ZERO_ADDRESS], {"from": bob})
