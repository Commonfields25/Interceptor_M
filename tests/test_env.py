"""Unit tests for RL environment modules — Interceptor_M
Issue: #57
Coverage target: ≥ 80%
"""
import os, sys, pytest, yaml, importlib
from pathlib import Path

# Resolve project root
ROOT = Path(__file__).parent.parent

class TestEnvConfig:
    """Tests for env_config.yaml loading and validation."""

    def test_env_config_exists(self):
        cfg = Path("env_config.yaml")
        assert cfg.exists(), "env_config.yaml must exist at repo root"

    def test_env_config_valid_yaml(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)

    def test_reward_keys_present(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        reward = data.get("reward", {})
        assert "success" in reward
        assert "crash" in reward
        assert "survival" in reward
        assert reward["success"] > reward["crash"]

    def test_success_ratio_threshold(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        ratio = data["reward"]["target_success_ratio"]
        assert 0 <= ratio <= 1, "target_success_ratio must be in [0,1]"
        assert ratio == 0.80, "target must be ≥ 80%"

    def test_reset_triggers_present(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        reset = data.get("reset", {})
        assert reset.get("trigger_on_crash") is True
        assert reset.get("trigger_on_divergence") is True

    def test_divergence_threshold_range(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        thr = data["reset"]["divergence_threshold"]
        assert 0 < thr <= 1.0

    def test_training_hyperparameters_present(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        train = data.get("training", {})
        assert "total_timesteps" in train
        assert "eval_episodes" in train
        assert train["eval_episodes"] == 1000

    def test_env_bounds_valid(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        env = data.get("env", {})
        assert env.get("max_altitude_m", 0) > env.get("min_altitude_m", 0)

    def test_dt_positive(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        assert data["env"]["sim_dt_s"] > 0

    def test_base_seed_set(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        assert data["reset"]["base_seed"] == 42


class TestEnvConfigIntegration:
    """Integration tests for reward shaping logic."""

    def test_reward_balance_success_vs_crash(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        r = data["reward"]
        # Crash penalty should be < success reward (numerically)
        assert abs(r["success"]) > abs(r["crash"])
        # Survival per step should be small positive
        assert 0 < r["survival"] < 1.0

    def test_max_episode_steps_reasonable(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        steps = data["reward"]["max_episode_steps"]
        assert steps >= 100, "max_episode_steps should allow meaningful episodes"

    def test_target_reward_in_training(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        target = data["training"]["target_reward"]
        # Should be positive and achievable
        assert target > 0

    def test_seed_strategy_valid(self):
        with open("env_config.yaml") as f:
            data = yaml.safe_load(f)
        valid = ["fixed", "sequential", "random"]
        assert data["reset"]["seed_strategy"] in valid


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])