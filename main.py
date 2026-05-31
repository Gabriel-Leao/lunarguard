import argparse
import time
import cv2

from detector.motion import MotionDetector
from detector.zone import ZoneManager
from detector.pose import FallDetector
from detector.blink import BlinkDetector
from ui.overlay import Overlay


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0")
    return parser.parse_args()


def open_capture(source: str):
    src = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir: {source}")
    return cap


def main():
    args = parse_args()
    cap  = open_capture(args.source)

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    motion_detector = MotionDetector(min_area=1500)
    zone_manager    = ZoneManager(frame_w, frame_h)
    fall_detector   = FallDetector()
    blink_detector  = BlinkDetector()
    overlay         = Overlay()

    show_zones = True
    prev_time  = time.time()

    last_fall_alert      = 0.0
    last_intrusion_alert = 0.0
    last_blink_alert     = 0.0
    ALERT_COOLDOWN       = 4.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        motion_boxes  = motion_detector.detect(frame)
        intrusions    = zone_manager.check_intrusion(motion_boxes)
        fall_detected = fall_detector.process(frame_rgb)
        eyes_closed   = blink_detector.process(frame_rgb)

        now = time.time()

        if fall_detected and (now - last_fall_alert) > ALERT_COOLDOWN:
            overlay.trigger_alert("ASTRONAUTA CAIDO / COLAPSO DETECTADO", duration=3.0)
            last_fall_alert = now

        if intrusions and (now - last_intrusion_alert) > ALERT_COOLDOWN:
            zone_names = ", ".join({z.name for z, _ in intrusions})
            overlay.trigger_alert(f"INTRUSAO EM ZONA RESTRITA: {zone_names}", duration=3.0)
            last_intrusion_alert = now

        if eyes_closed and (now - last_blink_alert) > ALERT_COOLDOWN:
            overlay.trigger_alert("ASTRONAUTA INCONSCIENTE / OLHOS FECHADOS", duration=3.0)
            last_blink_alert = now

        if show_zones:
            overlay.draw_zones(frame, zone_manager.zones)
            overlay.draw_legend(frame)

        overlay.draw_motion_boxes(frame, motion_boxes)
        overlay.draw_pose(frame, fall_detector.landmarks)
        overlay.draw_face(frame, blink_detector.face_landmarks)

        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 1e-9)
        prev_time = curr_time

        overlay.draw_hud(frame, fps=fps, fall=fall_detected,
                         intrusion=bool(intrusions), eyes_closed=eyes_closed)
        overlay.draw_alert(frame)

        cv2.imshow("LunarGuard", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            motion_detector = MotionDetector(min_area=1500)
        elif key == ord("z"):
            show_zones = not show_zones

    cap.release()
    fall_detector.close()
    blink_detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
