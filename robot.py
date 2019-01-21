import ctre
import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.frontLeft = ctre.WPI_TalonSRX(1)
        self.frontRight = ctre.WPI_TalonSRX(3)
        self.rearLeft = ctre.WPI_TalonSRX(2)
        self.rearRight = ctre.WPI_TalonSRX(4)

        self.spool = ctre.WPI_TalonSRX(5)

        #         self.rearLeft.setInverted(True)
        #         self.frontLeft.setInverted(True)

        self.drive = wpilib.RobotDrive(
            self.frontLeft, self.rearLeft, self.frontRight, self.rearRight
        )
        self.stick = wpilib.Joystick(0)

        self.pickUpHandler = 0
        self.pickupTimer = 0

        self.picker = wpilib.Solenoid(0, 1)
        self.rotation = wpilib.Solenoid(0, 2)
        self.thrust = wpilib.Solenoid(0, 3)
        self.transmission = wpilib.Solenoid(0, 4)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.arcadeDrive(self.stick.getRawAxis(1), self.stick.getRawAxis(2) ** 3)
        self.transmission.set(not self.stick.getRawButton(2))

        if self.stick.getRawButton(3):
            self.pickUpHandler = 0

        if self.pickUpHandler == 0:
            self.picker.set(True)
            self.rotation.set(True)
            self.thrust.set(False)

            if self.stick.getRawButtonPressed(1):
                self.pickUpHandler += 1
        elif self.pickUpHandler == 1:
            self.picker.set(False)
            if not self.stick.getRawButton(1):
                self.pickUpHandler += 1
        elif self.pickUpHandler == 2:
            self.picker.set(False)
            self.rotation.set(False)
            self.thrust.set(False)
            if self.stick.getRawButtonPressed(1):
                self.pickUpHandler += 1
        elif self.pickUpHandler == 3:
            self.picker.set(False)
            self.rotation.set(False)
            self.thrust.set(True)
            if self.stick.getRawButtonPressed(1):
                self.pickUpHandler += 1
        elif self.pickUpHandler == 4:
            self.picker.set(True)
            self.rotation.set(False)
            self.thrust.set(True)
            self.pickupTimer += 1
            if self.pickupTimer >= 15:
                self.pickUpHandler = 0
                self.pickupTimer = 0

        if self.stick.getRawButton(4):
            self.spool.set(-0.75)
        else:
            self.spool.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
