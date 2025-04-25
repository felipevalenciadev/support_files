# Author: Felipe Valencia

# Author: Felipe Valencia
# -*- coding: utf-8 -*-

from io.jans.service.cdi.util import CdiUtil # type: ignore
from io.jans.as.server.security import Identity # type: ignore
from io.jans.model.custom.script.type.auth import PersonAuthenticationType # type: ignore
from io.jans.as.server.service import AuthenticationService # type: ignore
from io.jans.as.server.service import UserService # type: ignore
from io.jans.util import StringHelper # type: ignore

import java # type: ignore
from datetime import datetime

class PersonAuthentication(PersonAuthenticationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, customScript,  configurationAttributes):
        print ("QS DEV - Initialization ...")
        print ("QS DEV - Initialized successfully")
        return True

    def destroy(self, configurationAttributes):
        print ("QS DEV - Destroy ...")
        print ("QS DEV - Destroyed successfully")
        return True

    def getAuthenticationMethodClaims(self, requestParameters):
        return None

    def getApiVersion(self):
        return 11

    def isValidAuthenticationMethod(self, usageType, configurationAttributes):
        return True

    def getAlternativeAuthenticationMethod(self, usageType, configurationAttributes):
        return None

    def authenticate(self, configurationAttributes, requestParameters, step):
        authenticationService = CdiUtil.bean(AuthenticationService)
        userService = CdiUtil.bean(UserService)
        identity = CdiUtil.bean(Identity)

        # -----------------
        # QS DEV - Get - CustomProperties

        # Login Attemps
        self.loginattempt = "loginattempt"
        if configurationAttributes.containsKey("login_attempt"):
            self.loginattempt = configurationAttributes.get("login_attempt").getValue2()
            print ("QS DEV - Initialization - Login Attempts: " + str(self.loginattempt))
        else:
            self.loginattempt = 5
            print ("QS DEV - Initialization - Using default attribute for Login Attempt: " + str(self.loginattempt))
        # Login Attemps

        # Time Attemp
        self.timeattempt = "timeattempt"
        if configurationAttributes.containsKey("time_attempt"):
            self.timeattempt = configurationAttributes.get("time_attempt").getValue2()
            print ("QS DEV - Initialization - Time Attempts: " + str(self.timeattempt))
        else:
            self.timeattempt = 5
            print ("QS DEV - Initialization - Using default attribute for Time Attempt: " + str(self.timeattempt))
        # Time Attemp

        # QS DEV - Get - CustomProperties
        # -----------------

        if (step == 1):
            print ("QS DEV - Authentication - Authenticate Step 1")
            credentials = identity.getCredentials()
            user_name = credentials.getUsername()
            user_password = credentials.getPassword()

            logged_in = False

            if (StringHelper.isNotEmptyString(user_name) and StringHelper.isNotEmptyString(user_password)):

                # QS DEV - Get User try to login
                foundUser = userService.getUserByAttribute("uid", user_name)
                # QS DEV - Validate Username for User
                if foundUser == None:
                    print ("QS DEV - Authentication - No se ha encontrado el usuario")
                    logged_in = False
                else:
                    # QS DEV - Obtener datos del usuario
                    email = foundUser.getAttribute("mail")
                    print("QS DEV - Authentication - Email: " + str(email))

                    # QS DEV - FuerzaBruta - Atributos para FuerzaBruta
                    timestamp = datetime.now()
                    formatted_timestamp = timestamp.strftime('%Y-%m-%d-%H-%M-%S')
                    loginAttempts = foundUser.getAttribute("qsloginattempt")
                    loginTimeStamp = foundUser.getAttribute("qslogintimestamp")
                    # QS DEV - FuerzaBruta - Verificar y manejar atributos vacios
                    if loginAttempts is None or loginAttempts == "":
                        loginAttempts = 0
                    else:
                        loginAttempts = int(loginAttempts)
                    if loginTimeStamp is None or loginTimeStamp == "":
                        loginTimeStamp = ""
                    else:
                        loginTimeStamp = str(loginTimeStamp)
                    # QS DEV - FuerzaBruta - Verificar y manejar loginAttempts
                    print("QS DEV - Authentication - Intentos de login: " + str(loginAttempts))
                    print("QS DEV - Authentication - Ultimo intento de login: " + str(loginTimeStamp))
                    # QS DEV - FuerzaBruta - Atributos para FuerzaBruta

                    # QS DEV - DO - Autentication - Si no ha superado el limite de inicios de sesion
                    if (loginAttempts < self.loginattempt):
                        logged_in = authenticationService.authenticate(user_name, user_password)
                    else:
                        logged_in = False
                    # QS DEV - DO - Autentication - Si no ha superado el limite de inicios de sesion

                if (logged_in):
                    # QS DEV - Autentication succes
                    return True
                else:
                    # QS DEV - Autenticacion fallida

                    # QS DEV - FuerzaBruta - Inicio
                    print("QS DEV - Autenticacion Fallida - Iniciando acciones por fuerza bruta...")

                    # QS DEV - FuerzaBruta - Condicional de bloqueo
                    if loginAttempts >= self.loginattempt:
                        print("QS DEV - Autenticacion Fallida - Usuario bloqueado por ataque de fuerza bruta")
                    else:
                        # QS DEV - FuerzaBruta - Validacion de intentos de login
                        print("QS DEV - Autenticacion Fallida - Registrando intento de fuerza bruta...")
                        if loginTimeStamp is not None and loginTimeStamp != "":
                            # Convertir loginTimeStamp a un objeto datetime
                            previous_timestamp = datetime.strptime(loginTimeStamp, '%Y-%m-%d-%H-%M-%S')
                            # Calcular la diferencia de tiempo en minutos
                            time_difference = (timestamp - previous_timestamp).total_seconds() / 60.0
                            if time_difference <= self.timeattempt:
                                loginAttempts += 1
                                print("QS DEV - Autenticacion Fallida - Nuevo intento de autenticacion fallida en MENOS de 5 minutos")
                            else:
                                loginAttempts = 1
                                print("QS DEV - Autenticacion Fallida - Nuevo intento de autenticacion fallida en MAS de 5 minutos")
                        else:
                            loginAttempts = 1

                        loginAttempts_str = str(loginAttempts)
                        foundUser.setAttribute("qsloginattempt", loginAttempts_str)
                        foundUser.setAttribute("qslogintimestamp", formatted_timestamp)
                        print("QS DEV - Autenticacion Fallida - Intento de fuerza bruta registrado en el horario: " + formatted_timestamp)
                        print("QS DEV - Autenticacion Fallida - Intentos de login: " + loginAttempts_str)
                        # QS DEV - FuerzaBruta - Validacion de intentos de login

                        # QS DEV - FuerzaBruta - Bloqueo por intentos maximos
                        if loginAttempts_str == str(self.loginattempt):
                            print("QS DEV - Autenticacion Fallida - Usuario bloqueado por limite maximo de intentos")
                        # QS DEV - FuerzaBruta - Bloqueo por intentos maximos

                        # QS DEV - FuerzaBruta - Actualizacion de usuario
                        userService.updateUser(foundUser)
                        # QS DEV - FuerzaBruta - Actualizacion de usuario

                    # QS DEV - FuerzaBruta - Fin

                    return False

        else:
            return False

    def prepareForStep(self, configurationAttributes, requestParameters, step):
        if (step == 1):
            print ("ProtectedAuth - Prepare for Step 1")
            return True
        else:
            return False

    def getExtraParametersForStep(self, configurationAttributes, step):
        return None

    def getCountAuthenticationSteps(self, configurationAttributes):
        return 1

    def getPageForStep(self, configurationAttributes, step):
        return ""

    def getNextStep(self, configurationAttributes, requestParameters, step):
        return -1

    def getLogoutExternalUrl(self, configurationAttributes, requestParameters):
        print ("ProtectedAuth - Get external logout URL call")
        return None

    def logout(self, configurationAttributes, requestParameters):
        return True
