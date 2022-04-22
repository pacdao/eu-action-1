// SPDX-License-Identifier: MIT
pragma solidity 0.8.7;
import "./imports.sol";

/* Bonus token for holders of any PAC DAO NFT */
contract PACDaoEUAction is ERC721Enumerable {

/* VARIABLES */
    uint256 public currentId;
    uint256 public mintPrice;

    bool public isActive;

    address payable public owner;
    address[] private _tokenAddrs;

    mapping(address => bool) public hasMinted;
    mapping(uint256 => string) private _tokenURIs;

    string public baseURI = "ipfs://";
    string public defaultMetadata = "QmavEQ84TMzbz7CEktD7SVE1vBQqeaBj4JGLXFgNmp3MPG";
    string private _contractURI = "QmXqtMKHL5AKQE8VhumF9aH5MeyPuwvd7m9KS5d22GKdhm";


/* CONSTRUCTOR */
    constructor (address payable init_owner, address[] memory init_tokenAddrs) ERC721 ("EU NFT", "PAC-EU"){
       owner = init_owner;
       _tokenAddrs = init_tokenAddrs;
       mintPrice = 42000000000000000;
       isActive = true;
    }


/* PUBLIC VIEWS */

    /**
     * @dev Returns eligible contracts for which users can claim a bonus if they have minted.
     *
     */
    function tokenAddrs() public view returns(address[] memory) {
	return _tokenAddrs;	
    }


    /**
     * @dev Returns number of NFTs the user would receive on mint.
     *
     */
    function isWhitelisted(address user) public view returns (bool) {
	uint count = 0;
	for(uint _i = 0; _i < _tokenAddrs.length; _i++) {
		address _addr = _tokenAddrs[_i];
		if(IERC721( _addr ).balanceOf(user) > 0) {
			count++;	
		}		
	}
	if(count > 0) {
	    return true;
	} else {
	    return false;
	}
    }

    /**
     * @dev Return token URI if set or Default URI
     *
     */
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
	require(_exists(tokenId)); // dev: "ERC721URIStorage: URI query for nonexistent token";

	string memory _tokenURI = _tokenURIs[tokenId];
	string memory base = baseURI;

	// If there is no base URI, return the token URI.
	if (bytes(base).length == 0 && bytes(_tokenURI).length > 0) {
	   return _tokenURI;
	}

	// If both are set, concatenate the baseURI and tokenURI (via abi.encodePacked).
	if (bytes(_tokenURI).length > 0) {
	   return string(abi.encodePacked(base, _tokenURI));
	}
	return string(abi.encodePacked(base, defaultMetadata)); 
    }

    /**
     * @dev Return contract URI
     *
     */
    function contractURI() public view returns(string memory) {
	return string(abi.encodePacked(baseURI, _contractURI));
    }
    

    function userPriceForQuantity(uint256 quantity, address addr) public view returns(uint256){
	require(quantity > 0); // dev: Non-zero Quantity Required
	if(isWhitelisted(addr) && hasMinted[msg.sender] == false) {
	   return((quantity - 1) * mintPrice);
	} else {
	   return(quantity * mintPrice);
	}

    }

/* PUBLIC WRITEABLE */

    /**
     * @dev Mint NFT if eligible.
     *
     */

    function mint(uint256 quantity) public payable
	{
		require(quantity > 0); // dev: No Quantity Specified
		require(isActive); // dev: Inactive
		require(msg.value >= userPriceForQuantity(quantity, msg.sender)); // dev: Insufficient Funds

		for(uint _i = 0; _i < quantity; _i++) {
			_mint(msg.sender);
		}
		if(isWhitelisted(msg.sender) && hasMinted[msg.sender] == false) {
			hasMinted[msg.sender] = true;
		}
	}

    /**
     * @dev Recover funds inadvertently sent to the contract
     *
     */
    function withdraw() public 
    {
		owner.transfer(address(this).balance);
    }


/* ADMIN FUNCTIONS */

    /**
     * @dev Admin function to mint an NFT for an address
     *
     */
    function updateMintPrice(uint256 _mintPrice) public payable
    {
	    require(msg.sender == owner); // dev: Only Admin
	    mintPrice = _mintPrice;
    }




    /**
     * @dev Admin function to mint an NFT for an address
     *
     */
    function mintFor(address _mintAddress) public payable
    {
	    require(msg.sender == owner); // dev: Only Admin
	    _mint(_mintAddress);
    }

    /**
     * @dev Transfer ownership to new admin
     *
     */
    function updateBeneficiary(address payable _newBeneficiary) public 
    {		
	require(msg.sender == owner); // dev: Only Admin
	owner = _newBeneficiary;
    }

    /**
     * @dev Stoke token URL for specific token
     *
     */
    function setTokenUri(uint256 _tokenId, string memory _newUri) public 
    {
	require(msg.sender == owner); // dev: Only Admin
	_setTokenURI(_tokenId, _newUri);
    }

    /**
    * @dev Update default token URL when not set
    *
    */
    function setDefaultMetadata(string memory _newUri) public 
    {
	require(msg.sender == owner); // dev: Only Admin
	defaultMetadata = _newUri;
    }

    /**
    * @dev Update contract URI
    *
    */
    function setContractURI(string memory _newData) public {
	require(msg.sender == owner); // dev: Only Admin
	_contractURI = _newData;
    }	    

    /**
    * @dev Update contract active
    *
    */
    function setIsActive(bool flag) public {
	require(msg.sender == owner); // dev: Only Admin
	isActive = flag;
    }	    


    /**
    * @dev Update eligible token addresses to receive mint
    *
    */
    function updateTokenAddrs(address[] memory _newTokenAddrs) public {
	require(msg.sender == owner); // dev: Only Admin
	_tokenAddrs = _newTokenAddrs;
    }


/* INTERNAL FUNCTIONS */

    /**
    * @dev Update ID and mint
    *
    */
    function _mint(address _mintAddress) private {
	currentId += 1;
	_safeMint(_mintAddress, currentId);
    }


    /**
     * @dev Sets `_tokenURI` as the tokenURI of `tokenId`.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal virtual {
        require(_exists(tokenId)); // dev: ERC721URIStorage: URI set of nonexistent token
        _tokenURIs[tokenId] =  _tokenURI;
    }


/* FALLBACK */
	receive() external payable { }
	fallback() external payable { }


}
