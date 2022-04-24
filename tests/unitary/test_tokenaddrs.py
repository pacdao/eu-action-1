import brownie


def test_update_with_gov_token(nft_gov, gov_addr):
    assert nft_gov.whitelist_tokens(0) == gov_addr


def test_gov_token_can_mint(nft_gov, gov_holder, nft):
    price = nft_gov.user_price_for_quantity(1, gov_holder)
    assert price == 0
    nft_gov.mint(1, {"from": gov_holder, "value": price})
    assert nft.balanceOf(gov_holder) > 0


def test_non_gov_token_cannot_mint(nft_gov, accounts):
    assert nft_gov.is_whitelisted(accounts[2]) == False
    with brownie.reverts():
        nft_gov.mint(1, {"from": accounts[2]})
