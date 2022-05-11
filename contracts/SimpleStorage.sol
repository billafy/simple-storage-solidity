// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract SimpleStorage {
    uint256 num;

    struct Person {
        string name;
        uint256 favouriteNumber;
    }

    mapping(string => Person) people;

    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people[_name] = Person(_name, _favouriteNumber);
    }

    function getPerson(string memory _name) public view returns(Person memory) {
        return people[_name];
    }

    function getNum() public view returns(uint256) {
        return num;
    }
}