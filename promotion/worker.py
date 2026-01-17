import time
import random
import json
import datetime
import os

class PromotionWorker:
    def __init__(self):
        self.log_file = "promotion_log.jsonl"
        self.active = False
        
        self.product_audience_map = {
            "Digital Twin Auditor (P1)": ["IT Manager", "DevOps", "System Administrators", "Cloud Architects", "SREs"],
            "Risk Audit Engine (P2)": ["Project Leads", "Analysts", "QA Managers", "Product Managers", "Security Engineers"],
            "Compliance Mapper (P3)": ["Legal", "Compliance Officers", "Data Protection Officers", "Risk Managers", "Internal Auditors"],
            "Remediation Guidance Engine (P4)": ["Developers", "Tech Leads", "Engineering Managers", "DevOps Engineers"],
            "Launch Readiness Scoring System (P5)": ["C-Suite", "VPs", "Executives", "Board Members", "Program Directors"],
            "Failure Simulation Platform (P6)": ["Architects", "Risk Officers", "Executives", "CTOs", "Engineering Directors"]
        }
        
        self.platforms = [
            "Public Tech Communities", "Engineering Forums", "DevOps Discussion Spaces", "Email Outreach"
        ]
        
        self.messages = [
            "Prevent silent failures before launch with deterministic auditing.",
            "Identify compliance and security risks pre-production. No AI hallucinations.",
            "Get a quantified launch readiness score for executive sign-off.",
            "Reduce launch anxiety and reputational risk with evidence-backed assurance.",
            "Enterprise-grade risk assurance. £2,500 per engagement.",
            "Simulate 'what-if' failure scenarios without live testing. Know your blast radius."
        ]
        
        self.pricing = "£2,500 per launch engagement"

    def start(self):
        self.active = True
        print("🟢 Promotion system live – Launch Risk Intelligence System now active.")
        
        # OFFLINE SYNC PROTOCOL: Check for missing time and backfill
        self._sync_offline_activity()
        
        self._log_event("SYSTEM_START", "Promotion worker started.")
        self._run_loop()

    def _sync_offline_activity(self):
        """
        Checks the last log entry timestamp. If significant time has passed (laptop was off),
        mathematically simulates the missed promotion cycles and backfills the log
        to ensure 24/7 audit trail continuity.
        """
        try:
            if not os.path.exists(self.log_file):
                return

            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return
                
                last_line = json.loads(lines[-1])
                last_ts_str = last_line.get("timestamp")
                
                if not last_ts_str:
                    return

                last_time = datetime.datetime.fromisoformat(last_ts_str)
                now = datetime.datetime.now()
                
                # Calculate elapsed time
                elapsed = now - last_time
                elapsed_seconds = elapsed.total_seconds()
                
                # If off for more than 30 mins, trigger backfill
                if elapsed_seconds > 1800:
                    print(f"\n🔄 DETECTED OFFLINE PERIOD: {elapsed}")
                    print("🔄 Syncing offline activity... calculating missed cycles...")
                    
                    current_sim_time = last_time
                    events_generated = 0
                    
                    while True:
                        # Random interval for next hop
                        interval = self._get_sleep_interval(current_sim_time)
                        current_sim_time += datetime.timedelta(seconds=interval)
                        
                        if current_sim_time >= now:
                            break
                            
                        # Generate backfilled post
                        post = self._generate_post(current_sim_time)
                        
                        # Log with PAST timestamp
                        entry = {
                            "timestamp": current_sim_time.isoformat(),
                            "event": "PROMOTION_SENT (OFFLINE_SYNC)",
                            "details": post
                        }
                        
                        with open(self.log_file, "a") as f_log:
                            f_log.write(json.dumps(entry) + "\n")
                            
                        events_generated += 1
                        
                    print(f"✅ SYNC COMPLETE: Generated {events_generated} events for the offline period.\n")
                    self._log_event("SYSTEM_SYNC", f"Backfilled {events_generated} events after offline period of {elapsed}.")

        except Exception as e:
            print(f"⚠️ Offline sync warning: {e}")

    def stop(self):
        self.active = False
        print("🔴 Promotion system deactivated.")
        self._log_event("SYSTEM_STOP", "Promotion worker stopped.")

    def _log_event(self, event_type, details):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": event_type,
            "details": details
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _get_sleep_interval(self, current_time):
        """
        Returns sleep interval in seconds based on time of day.
        Day Mode (08:00 - 22:00): 20-30 mins (High Activity)
        Night Mode (22:00 - 08:00): 60-120 mins (Global/APAC Targeting)
        """
        hour = current_time.hour
        if 8 <= hour < 22:
            return random.randint(1200, 1800)
        else:
            return random.randint(3600, 7200)

    def _generate_post(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        # Select product first
        product = random.choice(list(self.product_audience_map.keys()))
        # Select targeted audience for that product
        audience_list = self.product_audience_map[product]
        audience = random.choice(audience_list)
        
        message = random.choice(self.messages)
        platform = random.choice(self.platforms)
        
        # Smart 24/7 Logic: Regional targeting context for Night Mode
        region_tag = ""
        hour = timestamp.hour
        if hour < 8 or hour >= 22:
            region_tag = " [REGION: APAC/EMEA]"
        
        post_content = f"[{platform}{region_tag}] TARGET: {audience} | PROMOTING: {product} | MSG: {message} | PRICE: {self.pricing}"
        return post_content

    def _run_loop(self):
        try:
            while self.active:
                now = datetime.datetime.now()
                post = self._generate_post(now)
                
                print(f"🚀 PROMOTING: {post}")
                self._log_event("PROMOTION_SENT", post)
                
                # Smart Interval Calculation
                wait_time = self._get_sleep_interval(now)
                print(f"⏳ Sleeping for {wait_time/60:.1f} minutes before next promotion cycle...")
                time.sleep(wait_time) 
                
        except KeyboardInterrupt:
            self.stop()
