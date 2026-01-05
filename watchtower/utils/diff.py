"""Diff computation for runs and artifacts."""

from typing import Dict, Any, List, Set
from watchtower.models.claim import Claim
from watchtower.models.artifact import Artifact
import json


def compute_run_diff(claims_a: List[Claim], claims_b: List[Claim]) -> Dict[str, Any]:
    """
    Compute differences between two runs (sets of claims).
    
    Args:
        claims_a: Claims from first run
        claims_b: Claims from second run
        
    Returns:
        Dictionary containing diff information
    """
    # Create maps for easy comparison
    claims_a_map = {c.id: c for c in claims_a if c.id}
    claims_b_map = {c.id: c for c in claims_b if c.id}
    
    # Find added, removed, and modified claims
    ids_a = set(claims_a_map.keys())
    ids_b = set(claims_b_map.keys())
    
    added_ids = ids_b - ids_a
    removed_ids = ids_a - ids_b
    common_ids = ids_a & ids_b
    
    # Check for modifications
    modified_claims = []
    for claim_id in common_ids:
        claim_a = claims_a_map[claim_id]
        claim_b = claims_b_map[claim_id]
        
        # Compare key fields
        if (claim_a.statement != claim_b.statement or
            claim_a.confidence != claim_b.confidence or
            claim_a.run_fingerprint != claim_b.run_fingerprint):
            
            modified_claims.append({
                "id": claim_id,
                "statement_changed": claim_a.statement != claim_b.statement,
                "confidence_changed": claim_a.confidence != claim_b.confidence,
                "confidence_delta": claim_b.confidence - claim_a.confidence,
                "fingerprint_changed": claim_a.run_fingerprint != claim_b.run_fingerprint,
            })
    
    return {
        "added_claims": list(added_ids),
        "removed_claims": list(removed_ids),
        "modified_claims": modified_claims,
        "total_changes": len(added_ids) + len(removed_ids) + len(modified_claims),
    }


def compute_artifact_diff(artifact_a: Artifact, artifact_b: Artifact) -> Dict[str, Any]:
    """
    Compute differences between two artifacts.
    
    Args:
        artifact_a: First artifact
        artifact_b: Second artifact
        
    Returns:
        Dictionary containing diff information
    """
    diff = {
        "id_match": artifact_a.id == artifact_b.id,
        "type_match": artifact_a.artifact_type == artifact_b.artifact_type,
        "content_match": artifact_a.content == artifact_b.content,
        "sha256_match": artifact_a.sha256 == artifact_b.sha256,
        "fingerprint_match": artifact_a.fingerprint == artifact_b.fingerprint,
        "parent_match": artifact_a.parent_artifact_id == artifact_b.parent_artifact_id,
    }
    
    # Add content differences if different
    if not diff["content_match"]:
        try:
            content_a = json.loads(artifact_a.content)
            content_b = json.loads(artifact_b.content)
            diff["content_diff"] = _compute_dict_diff(content_a, content_b)
        except (json.JSONDecodeError, TypeError):
            diff["content_diff"] = "Raw content differs"
    
    return diff


def _compute_dict_diff(dict_a: Dict[str, Any], dict_b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute differences between two dictionaries.
    
    Args:
        dict_a: First dictionary
        dict_b: Second dictionary
        
    Returns:
        Dictionary containing diff information
    """
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())
    
    added_keys = keys_b - keys_a
    removed_keys = keys_a - keys_b
    common_keys = keys_a & keys_b
    
    modified_keys = []
    for key in common_keys:
        if dict_a[key] != dict_b[key]:
            modified_keys.append({
                "key": key,
                "old_value": dict_a[key],
                "new_value": dict_b[key],
            })
    
    return {
        "added_keys": list(added_keys),
        "removed_keys": list(removed_keys),
        "modified_keys": modified_keys,
    }
