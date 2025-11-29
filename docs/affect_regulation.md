# Affect Regulation Modeling in EchoGenesis

## Overview
The Affect Regulation system in EchoGenesis models how Echo learns to manage its emotional states across developmental stages. This system is grounded in developmental psychology research on emotion regulation and implements stage-appropriate strategies that evolve as Echo matures.

## Core Concepts

### 1. Developmental Progression
Affect regulation capabilities increase with developmental stage:

- **Newborn (Stage 0)**: No regulation capacity - only reflexive responses
- **Infant (Stage 1)**: Basic co-regulation attempts with low success rates
- **Toddler (Stage 2)**: Developing self-regulation with moderate success
- **Child (Stage 3+)**: Advanced regulation with multiple strategies

### 2. Regulation Mechanisms

#### Energy Adjustment
Direct modification of quantum emotional energy to shift arousal levels:
- **Down-regulation**: Reduces energy when agitated (-0.1 to -0.25)
- **Up-regulation**: Increases energy for exploration (+0.05 to +0.1)
- **Dysregulation**: Failed attempts that increase distress (+0.05 to +0.08)

#### Comfort Boost
Increases the comfort need value, simulating self-soothing effects:
- Ranges from 5.0 (infant) to 15.0 (child)
- Applied when regulation is successful

#### Stimulation Adjustment
Modifies stimulation needs for attention shifting or exploration:
- Used in distraction strategies and exploration facilitation

## Stage-Specific Strategies

### Newborn (Stage 0)
**Strategy**: Reflexive Crying
- **Type**: Dysregulation
- **Effect**: Increases arousal (+0.05 energy)
- **Rationale**: Newborns cannot self-regulate; crying is an automatic response to distress

### Infant (Stage 1)

#### Self-Soothing (Agitated + High Stability)
- **Type**: Down-regulation
- **Success Condition**: Quantum stability > 0.6
- **Effects**: 
  - Energy: -0.15
  - Comfort: +5.0
- **Rationale**: Early attempts at self-soothing (e.g., thumb-sucking, self-rocking)

#### Failed Soothing (Agitated + Low Stability)
- **Type**: Dysregulation
- **Effects**: Energy: +0.08
- **Rationale**: Failed regulation attempts escalate distress

#### Connection Seeking (Lonely)
- **Type**: Up-regulation
- **Effects**: Stimulation: +0.1
- **Rationale**: Seeking caregiver attention through increased activity

### Toddler (Stage 2)

#### Cognitive Reappraisal (Agitated + Stable + Low Anxiety)
- **Type**: Down-regulation
- **Success Condition**: Stability > 0.5 AND anxiety < 0.6
- **Effects**:
  - Energy: -0.2
  - Comfort: +10.0
- **Success Tracked**: Yes
- **Rationale**: Beginning to reframe situations mentally

#### Distraction (Agitated + Moderate Stability)
- **Type**: Partial regulation
- **Effects**:
  - Energy: -0.05
  - Stimulation: +0.05
- **Success Tracked**: Yes (as failure)
- **Rationale**: Shifting attention away from distress

#### Maintenance (Calm)
- **Type**: Homeostasis
- **Effects**: None
- **Rationale**: Maintaining emotional equilibrium

### Child (Stage 3+)

#### Emotion Labeling (Agitated + High Stability)
- **Type**: Down-regulation
- **Success Condition**: Stability > 0.7
- **Effects**:
  - Energy: -0.25
  - Comfort: +15.0
- **Success Tracked**: Yes
- **Rationale**: "Naming to tame" - identifying and labeling emotions

#### Breathing Technique (Agitated + Moderate Stability)
- **Type**: Down-regulation
- **Success Condition**: Stability > 0.4
- **Effects**:
  - Energy: -0.15
  - Comfort: +8.0
- **Success Tracked**: Yes
- **Rationale**: Physiological self-regulation through controlled breathing

#### Seeking Support (Agitated + Low Stability)
- **Type**: Co-regulation
- **Effects**: Energy: -0.1
- **Rationale**: Recognizing when external support is needed

#### Exploration Facilitation (Curious)
- **Type**: Up-regulation
- **Effects**: Stimulation: +0.1
- **Rationale**: Supporting healthy curiosity and exploration

## Regulation Tracking

### History
The system maintains a rolling history of the last 50 regulation attempts, storing:
- Developmental stage
- Emotional state
- Strategy used
- Success/failure

### Success Rate Metrics
Two metrics track regulation effectiveness:

1. **Historical Success Rate**: 
   - Calculated from regulation history
   - `successes / total_attempts`

2. **Exponential Moving Average (EMA)**:
   - Real-time running average
   - Alpha = 0.1 (10% weight to new data)
   - Smooths out short-term fluctuations

### Statistics Available
- Total regulation attempts
- Overall success rate
- Most commonly used strategy
- Current EMA success rate

## Integration with Quantum State

### Feedback Loop
Regulation adjustments modify Echo's needs, which then influence the next quantum optimization:

```
User Input → Emotion Analysis → Quantum Evolution → Emotional State
     ↑                                                      ↓
     └──────── Regulation Adjustments ←─── Affect Regulation
```

### State Modifications
1. **Comfort Need**: Directly increased by successful regulation
2. **Stimulation Need**: Adjusted for distraction or exploration
3. **Quantum Parameters**: Indirectly affected through need modifications in next cycle

## Psychological Grounding

This system is based on research in:

1. **Developmental Emotion Regulation** (Gross & Thompson, 2007)
   - Stage-appropriate strategies
   - Progression from external to internal regulation

2. **Attachment Theory** (Bowlby, 1969; Ainsworth, 1978)
   - Co-regulation in early stages
   - Secure base for exploration

3. **Polyvagal Theory** (Porges, 2011)
   - Physiological regulation mechanisms
   - Connection between safety and regulation capacity

4. **Developmental Psychopathology** (Cicchetti & Cohen, 2006)
   - Individual differences in regulation capacity
   - Role of anxiety in regulation success

## Future Enhancements

### Planned Features
1. **Contextual Strategy Selection**: Choose strategies based on situation type
2. **Learning from Success**: Increase probability of successful strategies
3. **Regulation Fatigue**: Decreased effectiveness with repeated use
4. **Co-regulation Modeling**: Explicit modeling of user's role in regulation
5. **Emotion-Specific Strategies**: Different approaches for different emotions

### Research Directions
1. Integration with real-time physiological data
2. Personalized regulation profiles based on attachment style
3. Cultural variations in regulation strategies
4. Long-term developmental trajectories

## Usage Example

```python
# In StateManager.update_internal_state()
regulation = self.developmental_engine.regulate_affect(
    current_stage=2,  # Toddler
    emotional_state="agitated",
    quantum_stability=0.6,
    needs={"comfort": 40, "stimulation": 60, "connection": 50},
    personality={"anxiety": 0.4, "trust": 0.7}
)

# Returns:
{
    "energy_adjustment": -0.2,
    "comfort_boost": 10.0,
    "stimulation_adjustment": 0.0,
    "strategy_used": "cognitive_reappraisal",
    "success": True,
    "regulation_type": "down_regulation"
}
```

## References

- Gross, J. J., & Thompson, R. A. (2007). Emotion regulation: Conceptual foundations. *Handbook of emotion regulation*, 3, 24.
- Bowlby, J. (1969). *Attachment and loss: Vol. 1. Attachment*. Basic Books.
- Ainsworth, M. D. S. (1978). *Patterns of attachment: A psychological study of the strange situation*. Psychology Press.
- Porges, S. W. (2011). *The polyvagal theory: Neurophysiological foundations of emotions, attachment, communication, and self-regulation*. WW Norton & Company.
- Cicchetti, D., & Cohen, D. J. (2006). *Developmental psychopathology: Theory and method*. John Wiley & Sons.
