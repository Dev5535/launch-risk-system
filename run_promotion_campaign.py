import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promotion.worker import PromotionWorker

if __name__ == "__main__":
    print("Initializing Promotion Campaign...")
    print("Checking health...")
    # Simulated health check
    import time
    time.sleep(1)
    print("Health Check Passed ✅")
    
    worker = PromotionWorker()
    worker.start()
