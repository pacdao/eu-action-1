# @version 0.3.3
# @dev EU Minter Logic
# @author pacdao.eth
# @license MIT

interface NFT:
    def balanceOf(addr: address) -> uint256: view
    def mint(addr: address) -> bool: nonpayable
    def setTokenURI(tokenId: uint256, newURI: String[128]): nonpayable
    def setContractURI(newURI: String[128]): nonpayable
    def setDefaultMetadata(newURI: String[128]): nonpayable
    def transferOwner(newAddr: address): nonpayable
    def transferMinter(newAddr: address): nonpayable

NFT_ADDR: immutable(address)
MAX_MINT: immutable(uint256)

mint_price: public(uint256)
whitelist_tokens: public(DynArray[address, 4])
owner: public(address)
is_active: public(bool)
has_minted: public(HashMap[address, bool])


@external
def __init__(nft_addr: address, whitelist_tokens: DynArray[address, 4]):
    NFT_ADDR = nft_addr
    MAX_MINT = 10
    self.owner = msg.sender
    self.mint_price = 42000000000000000
    self.whitelist_tokens = whitelist_tokens
    self.is_active = True


@external
@payable
def __default__():
    pass


@external
@pure
def nft_addr() -> address:
    return NFT_ADDR


@internal
@view
def _is_whitelisted(user: address) -> bool:
    for addr in self.whitelist_tokens:
        if NFT(addr).balanceOf(user) > 0:
            return True
    return False


@external
@view
def is_whitelisted(user: address) -> bool:
    return self._is_whitelisted(user)


@internal
@view
def _user_price_for_quantity(quantity: uint256, user: address) -> uint256:
    assert quantity > 0  # dev: Non-zero Quantity Required
    if self._is_whitelisted(user) and self.has_minted[user] == False:
        return (quantity - 1) * self.mint_price
    else:
        return quantity * self.mint_price


@external
@view
def user_price_for_quantity(quantity: uint256, user: address) -> uint256:
    return self._user_price_for_quantity(quantity, user)


@internal
def _mint(addr: address):
    NFT(NFT_ADDR).mint(addr)


@external
@payable
def mint(quantity: uint256):
    assert quantity > 0  # dev: No Quantity Specified
    assert quantity < MAX_MINT  # dev: Too many mints
    assert self.is_active  # dev: Inactive
    assert msg.value >= self._user_price_for_quantity(
        quantity, msg.sender
    )  # dev: Insufficient Funds

    for i in range(10):
        if i >= quantity:
            break
        self._mint(msg.sender)

    if self._is_whitelisted(msg.sender) and self.has_minted[msg.sender] == False:
        self.has_minted[msg.sender] = True


@external
def mint_for(mint_address: address):
    assert msg.sender == self.owner  # dev: Only Admin
    self._mint(mint_address)


@external
def withdraw():
    send(self.owner, self.balance)


@external
def set_mint_price(mint_price: uint256):
    assert msg.sender == self.owner  # dev: Only Admin
    self.mint_price = mint_price


@external
def set_owner(new_owner: address):
    assert msg.sender == self.owner  # dev: Only Admin
    self.owner = new_owner

@external
def set_nft_owner(new_owner: address):
    assert msg.sender == self.owner  # dev: Only Admin
    NFT(NFT_ADDR).transferMinter(new_owner)


@external
def set_nft_minter(new_owner: address):
    assert msg.sender == self.owner  # dev: Only Admin
    NFT(NFT_ADDR).transferMinter(new_owner)


@external
def set_token_uri(token_id: uint256, new_uri: String[128]):
    assert msg.sender == self.owner  # dev: Only Admin
    NFT(NFT_ADDR).setTokenURI(token_id, new_uri)


@external
def set_contract_uri(new_uri: String[128]):
    assert msg.sender == self.owner  # dev: Only Admin
    NFT(NFT_ADDR).setContractURI(new_uri)


@external
def set_is_active(is_active: bool):
    assert msg.sender == self.owner  # dev: Only Admin
    self.is_active = is_active


@external
def set_whitelist_addrs(tokens: DynArray[address, 4]):
    assert msg.sender == self.owner  # dev: Only Admin
    self.whitelist_tokens = tokens


@external
def set_default_metadata(new_uri: String[128]):
    assert msg.sender == self.owner  # dev: Only Admin
    NFT(NFT_ADDR).setDefaultMetadata(new_uri)
