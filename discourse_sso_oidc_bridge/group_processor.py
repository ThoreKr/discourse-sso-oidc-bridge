from typing import Dict, List


def process_group_mappings(
    group_mapping_config: Dict[str, dict], sso_attributes: dict, groups: List[str]
):
    """Processes the groups from the mapping rule config into discourse compatible formats

    Args:
        group_mapping_config (Dict[str, dict]): Predefined mapping rules for the keycloak group tree
            {
                "<group_name>": {
                    "name": "<group name in discourse>",
                    "isMod": false,
                    "isAdmin": false
                },
                ...
            }
        sso_attributes (dict): SSO Attributes as they will be processed by the bridge
        groups (List[str]): List of groups from the userinfo endpoint
    """
    grps = list()
    for group in groups:
        mapping_rule = group_mapping_config.get(group)

        if mapping_rule is None:
            continue

        elif mapping_rule.get("isAdmin", False):
            sso_attributes["admin"] = "true"
        if mapping_rule.get("isMod", False):
            sso_attributes["moderator"] = "true"
        else:
            grps.append(mapping_rule["name"])

        # Make sure the mod and admin privileges are pinned to false to trigger permission reset on group change.
        for priv in ["admin", "moderator"]:
            if priv not in sso_attributes:
                sso_attributes[priv] = "false"

    sso_attributes["groups"] = ",".join(grps)
    return sso_attributes
