// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;
/// @notice Accord 2-sur-3 lié à un retrait précis, pas une autorisation globale.
contract TreasuryGuard {
    address[3] public signers;
    mapping(address => bool) public isSigner;
    mapping(bytes32 => mapping(address => bool)) public approvedBy;
    mapping(bytes32 => uint8) public approvals;
    event ApprovalChanged(bytes32 indexed key, address indexed signer, bool approved, uint8 count);
    constructor(address[3] memory signers_) {
        for (uint256 i; i < 3; ++i) {
            require(signers_[i] != address(0) && !isSigner[signers_[i]], "invalid signer");
            signers[i] = signers_[i]; isSigner[signers_[i]] = true;
        }
    }
    function withdrawalKey(address core, uint256 id, address beneficiary, uint256 amount) public view returns(bytes32) {
        return keccak256(abi.encode(block.chainid, core, id, beneficiary, amount));
    }
    function setApproval(address core, uint256 id, address beneficiary, uint256 amount, bool approved) external {
        require(isSigner[msg.sender], "not signer");
        bytes32 key = withdrawalKey(core, id, beneficiary, amount);
        require(approvedBy[key][msg.sender] != approved, "unchanged");
        approvedBy[key][msg.sender] = approved;
        if (approved) approvals[key]++; else approvals[key]--;
        emit ApprovalChanged(key, msg.sender, approved, approvals[key]);
    }
    function isApproved(address core, uint256 id, address beneficiary, uint256 amount) external view returns(bool) {
        return approvals[withdrawalKey(core, id, beneficiary, amount)] >= 2;
    }
}
