# PAC DAO EU Action 1

Mint an EU Action NFT for PAC DAO

* [🌐  Web](https://pac.xyz/)
* [🎮  Discord ](https://discord.gg/tbBKXQqm)
* [🛫  Telegram ](https://t.me/joinchat/VYYqN19O3Wc4OTZh)
* [🦅  Twitter](https://twitter.com/pacdao)

The EU Parliament is [cracking down on cryptocurrency](https://twitter.com/paddi_hansen/status/1507741879563132928).  Inspired by our successful [SEC Letter Writing campaign](https://pac.xyz/#/sec-action), PAC DAO is announcing a similar campaign targeted at users who help EU citizens organize and respectfully comment to Parliament.

# NFT Giveaway

![PAC DAO](Scooby.png)

To raise awareness, PAC DAO is offering a free (+gas) mint of this NFT by artist [Scooby Doomer](https://opensea.io/collection/ct-all-stars) for anybody who fulfills any of the following criteria:

1. has left more than 3 qualified candidate ratings on [pac.xyz](https://pac.xyz/) or [eu.pac.xyz](https://eu.pac.xyz/) as of snapshot time
2. submits a letter to their member of Parliament (redeem via Discord)
3. holds a PAC DAO founder token or any quantity of PAC DAO gov tokens

All others may mint for the price of 0.042 -- with all funds being dedicated to support EU Activism via determination by the DAO

[OpenSea](https://opensea.io/collection/pacdao-eu-action-nft-1) | [Minter Contract](https://etherscan.io/address/0xbd760296c54e7c910d0f181b92ad704ff109fa01) | [NFT Contract](https://etherscan.io/address/0xb5e746af9ef99570df97380c5601ede0011f25a1)

### Eligible Tokens

 * [Founder NFT](https://etherscan.io/address/0x63994B223F01b943eFf986b1B379312508dc15F8)
 * [Governance Token](https://etherscan.io/address/0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b)

### Instructions
At the moment, no frontend interface for minting is available.  To mint, visit the Etherscan page for the minter deployment address (coming soon) and follow the steps:

1. Get the mint price for the quantity you wish to mint via the `user_price_for_quantity`
2. Call the `mint` function with this value of ETH (or more)

# Developer Notes

This NFT is itself historic.  Due to differences in byte types, no prior ERC-721 coded in Vyper was compatible or successfully indexed by OpenSea.  Since the release of the Vyper 0.3.2, Vyper became fully compatible.  This NFT is therefore the first known NFT to be available on OpenSea.

NFTs coded in Vyper have significant advantages, including gas savings.  Even with full ERC721-Enumerable compatibility, the gas price of this mint is lower than any known Solidity NFT.

The [contract/VyperNFT.vy](https://github.com/pacdao/eu-action-1/blob/main/contracts/VyperNFT.vy) file in this repository extends the functionality of the [Vyper NFT Example](https://github.com/vyperlang/vyper/blob/master/examples/tokens/ERC721.vy) with ERC721-Enumerable compatibility.  This file may be modified and used by any parties wishing to generate their own Vyper NFT with its efficiency.  The [contract/EUMinter.vy](https://github.com/pacdao/eu-action-1/blob/main/contracts/EUMinter.vy) implements custom minting logic.

Please note that the contract has not been through any audits or rigorous testing.  As the first of its type to be deployed, this remains a highly experimental implementation and users should consider this NFT extremely risky.  Neither PAC DAO nor Vyper assume any responsibility for loss of funds or collectibles from interacting with this NFT contract.

*PAC (People Advocating for Crypto) is a grassroots issue based activism DAO dedicated to furthering crypto adoption worldwide. PAC is not a Political Action Committee, and nothing expressed in PAC’s website or other public forums shall be construed as such. Further, this website and any other public PAC forums, including content such as proposals supported by PAC, the PAC Pro-Crypto Scorecard, and Bills and Campaigns discussed by PAC, are for informational purposes only. The NFT is obtained by supporters of PAC “as is” and without warranties of any kind. PAC is not liable for any harm caused by participation therein, or by obtaining a Founding Member NFT. By obtaining the NFT, you agree that you are not obtaining a security or investment instrument, you have undertaken your own review of laws applicable to you in your jurisdiction and confirm that your action is permissible under such applicable laws and you are obtaining the NFT for your own account without intent to distribute the NFT to third parties.*
