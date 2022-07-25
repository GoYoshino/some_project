from typing import List
import logging

logger = logging.getLogger(__name__)

def concat_7bits(byte_list: List[int]):

    if len(byte_list) == 1:
        return byte_list[0] & 0b01111111

    reversed_byte_list = byte_list.copy()
    reversed_byte_list.reverse()
    logger.debug(reversed_byte_list)
    number = reversed_byte_list[0]
    logger.debug(f"starting value: {bin(number)} = {number}")

    for byte in reversed_byte_list[1:]:
        assert byte >= 0
        assert byte <= 255
        seven_bit = byte & 0b01111111
        logger.debug(f"list value: {bin(byte)} = {byte}")
        logger.debug(f"after mask: {seven_bit} = {seven_bit}")

        number = number << 7
        logger.debug(f"shifted: {bin(number)} = {number}")
        number = number | seven_bit
        logger.debug(f"concatted: {bin(number)} = {number}")

    return number

def divide_to_7bits(number: int) -> List[int]:

    byte_list = []

    while (True):
        logger.debug(f"number: {bin(number)} = {hex(number)}")

        if number > 128:
            new_number = 0b10000000 | (number & 0b1111111)
            byte_list.append(new_number)
            logger.debug(f"number to be added: {bin(new_number)} = {hex(new_number)}")
            number = number >> 7
            logger.debug(f"shifted to: {bin(number)} = {hex(number)}")
        else:
            new_number = number
            logger.debug(f"number to be added: {bin(new_number)} = {hex(new_number)}")
            byte_list.append(new_number)
            break

    return byte_list