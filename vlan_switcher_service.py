"""
This module provides compatibility for the VLANSwitcher service.
It imports the SecureVLANSwitcherService from secure_vlan_switcher.py and
exposes it as VLANSwitcher for backward compatibility.
"""

from secure_vlan_switcher import SecureVLANSwitcherService as VLANSwitcher

# Re-export the VLANSwitcher class for compatibility
__all__ = ['VLANSwitcher']
