#include "apimanager.h"
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonObject>
#include <QJsonDocument>
#include <QDebug>
#include <QFile>
#include <QJsonArray>

ApiManager::ApiManager(QObject *parent)
    : QObject(parent), networkManager(new QNetworkAccessManager)
{
}

ApiManager::~ApiManager()
{
    delete networkManager;
}

static const QString apiAdressLogin = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/login/";
static const QString apiAddresLogout = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/logout/";
static const QString apiAddresRegister = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/user/";

//Forgot Password
static const QString apiAddresForgotPassword = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/user/forgot_password/";
static const QString apiAddresForgotPasswordCheckToken = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/user/forgot_password_check_token/";
static const QString apiAddresForgotPasswordConfirm = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/user/forgot_password_confirm/";
//Forgot Password

QByteArray ApiManager::prepareLoginData(const QString &login, const QString &password)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::loginUser(const QString &login, const QString &password)
{
    QNetworkRequest request{QUrl(apiAdressLogin)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareLoginData(login, password);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleLoginResponse(reply);
        reply->deleteLater();
    });
}

void ApiManager::handleLoginResponse(QNetworkReply *reply)
{
    const auto jsonObject{parseResponseToJson(reply)};

    if (reply->error() == QNetworkReply::NoError) {

        if (jsonObject.contains("token")) {
            m_token = jsonObject["token"].toString();
            emit loginCorrect(m_token);
        } else {
            emit loginFailed("Token missing");
        }

    } else {
        emit loginFailed(getErrorResponseInString(jsonObject));
    }
}

QByteArray ApiManager::prepareRegisterData(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    jsonObject["password2"] = passwordRepeated;
    jsonObject["email"] = emailAddress;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::registerUser(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress)
{
    QNetworkRequest request{QUrl(apiAddresRegister)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareRegisterData(login, password, passwordRepeated, emailAddress);

    QNetworkReply *reply = networkManager->post(request, requestData);
    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleRegisterResponse(reply);
        reply->deleteLater();
    });

}

void ApiManager::handleRegisterResponse(QNetworkReply *reply){
    if (reply->error() == QNetworkReply::NoError) {
        emit registerCorrect();
    } else {
        const auto jsonObject{parseResponseToJson(reply)};
        emit registerFailed(getErrorResponseInString(jsonObject));
    }
}

void ApiManager::logoutUser()
{
    if(m_token.isEmpty())
    {
        emit logoutFailed("Token missing");
        return;
    }

    QNetworkRequest request{QUrl(apiAddresLogout)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setRawHeader("Authorization", QByteArray("Token ").append(m_token.toUtf8()));
    QNetworkReply *reply = networkManager->post(request, QByteArray());

    connect(reply, &QNetworkReply::finished, [=]() {
        handleLogoutResponse(reply);
        reply->deleteLater();
    });
}

void ApiManager::handleLogoutResponse(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        this->m_token.clear();
        emit logoutCorrect();
    } else {
        const auto jsonObject{parseResponseToJson(reply)};
        emit logoutFailed(getErrorResponseInString(jsonObject));
    }
}

QByteArray ApiManager::prepareForgotPasswordData(const QString &emailAddress)
{
    QJsonObject jsonObject;
    jsonObject["email"] = emailAddress;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::forgotPassword(const QString &emailAddress)
{
    QNetworkRequest request{QUrl(apiAddresForgotPassword)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareForgotPasswordData(emailAddress);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleForgotPasswordResponse(reply);;
        reply->deleteLater();
    });
}

void ApiManager::handleForgotPasswordResponse(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        emit forgotPasswordCorrect();
    } else {
        const auto jsonObject{parseResponseToJson(reply)};
        emit forgotPasswordFailed(getErrorResponseInString(jsonObject));
    }
}

QByteArray ApiManager::prepareForgotPasswordCheckToken(const QString &emailAddress, const QString &code)
{
    QJsonObject jsonObject;
    jsonObject["email"] = emailAddress;
    jsonObject["token"] = code;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::forgotPasswordCheckToken(const QString &emailAddress, const QString &code)
{
    QNetworkRequest request{QUrl(apiAddresForgotPasswordCheckToken)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareForgotPasswordCheckToken(emailAddress, code);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleForgotPasswordCheckToken(reply);;
        reply->deleteLater();
    });
}

void ApiManager::handleForgotPasswordCheckToken(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        emit forgotPasswordCheckTokenCorrect();
    } else {
        const auto jsonObject{parseResponseToJson(reply)};
        emit forgotPasswordCheckTokenFailed(getErrorResponseInString(jsonObject));
    }
}

QByteArray ApiManager::prepareForgotPasswordConfirm(const QString &emailAddress, const QString &code, const QString &password, const QString &passwordRepeated)
{
    QJsonObject jsonObject;
    jsonObject["email"] = emailAddress;
    jsonObject["token"] = code;
    jsonObject["password"] = password;
    jsonObject["password2"] = passwordRepeated;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::forgotPasswordConfirm(const QString &emailAddress, const QString &code, const QString &password, const QString &passwordRepeated)
{
    QNetworkRequest request{QUrl(apiAddresForgotPasswordConfirm)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareForgotPasswordConfirm(emailAddress, code, password, passwordRepeated);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleForgotPasswordConfirm(reply);;
        reply->deleteLater();
    });
}

void ApiManager::handleForgotPasswordConfirm(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        emit forgotPasswordConfirmCorrect();
    } else {
        const auto jsonObject{parseResponseToJson(reply)};
        emit forgotPasswordConfirmFailed(getErrorResponseInString(jsonObject));
    }
}

QJsonObject ApiManager::parseResponseToJson(QNetworkReply* reply) {
    QByteArray responseData = reply->readAll();
    if (responseData.isEmpty()) {
        qDebug() << "Response data is empty";
        return QJsonObject();
    }

    QJsonParseError parseError;
    QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData, &parseError);
    if (parseError.error != QJsonParseError::NoError) {
        qDebug() << "Failed to parse JSON:" << parseError.errorString();
        return QJsonObject();
    }

    return jsonDocument.object();
}

QString ApiManager::getErrorMessages(const std::vector<QString>& errors){
    QString errorMsg{};
    const std::size_t errorsSize{errors.size()};

    for(size_t counter = 0 ; counter < errorsSize ; counter++)
    {
        errorMsg += errors.at(counter);
        if(errorsSize - 1 != counter)
           errorMsg+="\n";
    }

    return errorMsg;
}

std::vector<QString> ApiManager::parseErrorResponse(const QJsonObject& apiJsonResponse)
{
    std::vector<QString> errors{};

    for (const auto& key : apiJsonResponse.keys()) {
           QJsonValue value = apiJsonResponse[key];
           if (value.isArray())
           {
               QJsonArray jsonErrors = value.toArray();
               for (const auto& error : jsonErrors)
               {
                   if (error.isString())
                       errors.emplace_back(error.toString());
               }
           }
       }

    return errors;
}

QString ApiManager::getErrorResponseInString(const QJsonObject& apiJsonResponse)
{
    const auto error{parseErrorResponse(apiJsonResponse)};
    const QString errorMessages{getErrorMessages(error)};

    if(!errorMessages.isEmpty())
        return errorMessages;

    return "Check internet connection or restart the app";
}
