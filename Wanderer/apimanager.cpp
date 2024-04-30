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

QByteArray ApiManager::prepareLoginData(const QString &login, const QString &password)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    return QJsonDocument(jsonObject).toJson();
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
        const auto error{parseErrorApiResponse(jsonObject)};
        const QString errorMessages{getErrorMessages(error)};
        emit loginFailed(errorMessages);
    }
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

    const auto jsonObject{parseResponseToJson(reply)};

    if (reply->error() == QNetworkReply::NoError) {
        emit registerCorrect();
    } else {
        const auto error{parseErrorApiResponse(jsonObject)};
        const QString errorMessages{getErrorMessages(error)};
        emit registerFailed(errorMessages);
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
    const auto jsonObject{parseResponseToJson(reply)};

    if (reply->error() == QNetworkReply::NoError) {
        this->m_token.clear();
        emit logoutCorrect();
    } else {
        const auto error{parseErrorApiResponse(jsonObject)};
        const QString errorMessages{getErrorMessages(error)};
        emit logoutFailed(errorMessages);
    }
}

std::unordered_map<int, QString> ApiManager::parseErrorApiResponse(const QJsonObject &apiJsonResponse)
{
    std::unordered_map<int, QString> errorMap;

    if(apiJsonResponse.contains("errors"))
    {
        QJsonArray errors = apiJsonResponse["errors"].toArray();

        for(const auto& error : errors)
        {
            if(!error.isObject())
                continue;

            int errorCode = -1;
            QString errorMessage = "UndefinedError";

            if(error.toObject().contains("status"))
                errorCode = error.toObject()["status"].toInt();


            if(error.toObject().contains("error"))
                errorMessage = error.toObject()["error"].toString();

            errorMap[errorCode] = errorMessage;
        }
    }

    return errorMap;
}

QString ApiManager::getErrorMessages(const std::unordered_map<int, QString> &errorMap)
{
    QString errorMessages{};

    for(const auto& [_,errorMessage] : errorMap)
        errorMessages+=errorMessage+"\n";

    return errorMessages;
}

QJsonObject ApiManager::parseResponseToJson(QNetworkReply* reply){
    QByteArray responseData = reply->readAll();
    QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData);
    qDebug(responseData);
    return jsonDocument.object();
}



