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

const QString ApiAdressLogin = "https://bart-kris-api-test-84e163f71bea.herokuapp.com/api/v1/login/";
const QString apiAddresRegister = "https://bart-kris-api-test-84e163f71bea.herokuapp.com/api/v1/user/";

QByteArray ApiManager::prepareUserData(const QString &login, const QString &password)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    return QJsonDocument(jsonObject).toJson();
}

void ApiManager::loginUser(const QString &login, const QString &password)
{
    QNetworkRequest request{QUrl(ApiAdressLogin)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareUserData(login, password);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleLoginResponse(reply);
        reply->deleteLater();
    });
}

void ApiManager::handleLoginResponse(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        QByteArray responseData = reply->readAll();
        QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData);
        QJsonObject jsonObject = jsonDocument.object();

        if (jsonObject.contains("token")) {
            m_token = jsonObject["token"].toString();
            qDebug() << "Login Correct: " + m_token;
            emit loginCorrect(m_token);
        } else {
            qDebug() << "Token not found in JSON response.";
            emit loginFailed();
        }
    } else {
        qDebug() << "Error:" << reply->errorString();
        emit loginFailed();
    }
}

void ApiManager::registerUser(const QString &login, const QString &password)
{
    QNetworkRequest request{QUrl(apiAddresRegister)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareUserData(login,password);

    QNetworkReply *reply = networkManager->post(request, requestData);
    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleRegisterResponse(reply);
        reply->deleteLater();
    });

}

void ApiManager::handleRegisterResponse(QNetworkReply *reply){
    if (reply->error() == QNetworkReply::NoError) {
        qDebug() << "Response:" << reply->readAll();
        emit registerCorrect();
    } else {
        qDebug() << "Error:" << reply->errorString();
        emit registerFailed();
    }
}



