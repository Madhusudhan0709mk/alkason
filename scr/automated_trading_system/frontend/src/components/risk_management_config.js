step="0.1" 
            value={riskConfig.maxLeverage} 
            onChange={handleInputChange} 
          />
        </div>
        <div>
          <label>Risk Per Trade (%)</label>
          <input 
            name="riskPerTrade" 
            type="number" 
            step="0.1" 
            value={riskConfig.riskPerTrade} 
            onChange={handleInputChange} 
          />
        </div>
        <button type="submit">Update Risk Management Configuration</button>
      </form>
    </div>
  );
}

export default RiskManagementConfig;
